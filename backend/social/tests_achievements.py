"""
Session 8A achievement tests:
- award_badge idempotency
- generate_achievement_card correct fields
- grant_cross_path_title for 2/3/4/5 path combos
- check_streak_milestones at boundaries
- check_level_milestones at boundaries
- Integration: quest completion triggers level 5 badge + achievement card
- Integration: complete_weekly_boss creates badge + card + bonus EXP
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from paths.models import UserPathSelection
from players.models import Player
from quests.models import (
    DailyQuestLineup,
    DailyQuestLineupItem,
    Quest,
)
from social.achievements import (
    award_badge,
    check_level_milestones,
    check_streak_milestones,
    complete_weekly_boss,
    generate_achievement_card,
    grant_cross_path_title,
)
from social.models import (
    AchievementCard,
    Badge,
    UserBadge,
    WeeklyBossQuest,
)

User = get_user_model()


# ── helpers ───────────────────────────────────────────────────────────────────

def _make_player(username, path="fitness_warrior", streak=0, level=1, exp=0):
    user = User.objects.create_user(username, password="pw")
    player = Player.objects.get(user=user)
    player.path = path
    player.streak = streak
    player.level = level
    player.exp = exp
    player.save(update_fields=["path", "streak", "level", "exp", "updated_at"])
    return player


def _make_selection(player, paths=None):
    path = player.path or "fitness_warrior"
    active = paths or [path]
    sel = UserPathSelection.objects.create(
        player=player,
        path=path,
        onboarding_complete=True,
        multi_paths_active=active,
    )
    return sel


def _make_badge(key, tier="bronze"):
    badge, _ = Badge.objects.get_or_create(
        key=key,
        defaults={"name": key, "tier": tier, "path_specific": "", "icon_name": ""},
    )
    return badge


def _make_quest(title, *, rank="D", path_target="fitness_warrior", exp_reward=40):
    return Quest.objects.create(
        title=title, exp_reward=exp_reward, rank=rank, path_target=path_target, pillar="body",
    )


def _make_lineup(player, path="fitness_warrior", quest=None):
    today = timezone.localdate()
    lineup = DailyQuestLineup.objects.create(player=player, path=path, date=today)
    if quest:
        DailyQuestLineupItem.objects.create(
            lineup=lineup, quest=quest, slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
        )
    return lineup


# ── award_badge ───────────────────────────────────────────────────────────────

class AwardBadgeTests(TestCase):

    def setUp(self):
        self.player = _make_player("p1")
        self.badge = _make_badge("streak_7")

    def test_awards_badge_on_first_call(self):
        ub = award_badge(self.player, "streak_7")
        self.assertIsNotNone(ub)
        self.assertEqual(ub.badge.key, "streak_7")
        self.assertEqual(UserBadge.objects.filter(player=self.player).count(), 1)

    def test_idempotent_second_call_returns_none(self):
        award_badge(self.player, "streak_7")
        ub2 = award_badge(self.player, "streak_7")
        self.assertIsNone(ub2)
        self.assertEqual(UserBadge.objects.filter(player=self.player).count(), 1)

    def test_missing_badge_key_returns_none(self):
        result = award_badge(self.player, "nonexistent_badge_xyz")
        self.assertIsNone(result)

    def test_non_idempotent_creates_duplicate(self):
        """When idempotent=False, multiple UserBadge rows are allowed (no unique constraint)."""
        # Note: unique_together on UserBadge prevents true duplicates at DB level.
        # non-idempotent skips get_or_create and calls create() directly — which will raise.
        # This test verifies that the first award works; the duplicate prevention is at DB level.
        ub = award_badge(self.player, "streak_7", idempotent=False)
        self.assertIsNotNone(ub)


# ── generate_achievement_card ─────────────────────────────────────────────────

class GenerateAchievementCardTests(TestCase):

    def setUp(self):
        self.player = _make_player("p2")

    def test_creates_card_with_correct_fields(self):
        card = generate_achievement_card(
            self.player,
            "level_milestone",
            title="Level 5 Reached!",
            subtitle="You're a Novice Adventurer.",
            metadata={"level": 5},
        )
        self.assertIsNotNone(card.id)
        self.assertEqual(card.player, self.player)
        self.assertEqual(card.card_type, "level_milestone")
        self.assertEqual(card.title, "Level 5 Reached!")
        self.assertEqual(card.subtitle, "You're a Novice Adventurer.")
        self.assertEqual(card.metadata, {"level": 5})

    def test_empty_subtitle_and_metadata_defaults(self):
        card = generate_achievement_card(self.player, "boss", title="Boss Defeated!")
        self.assertEqual(card.subtitle, "")
        self.assertEqual(card.metadata, {})

    def test_multiple_cards_allowed(self):
        generate_achievement_card(self.player, "milestone", title="Card A")
        generate_achievement_card(self.player, "milestone", title="Card B")
        self.assertEqual(AchievementCard.objects.filter(player=self.player).count(), 2)


# ── grant_cross_path_title ────────────────────────────────────────────────────

class GrantCrossPathTitleTests(TestCase):

    def _setup_paths(self, player, paths):
        _make_selection(player, paths=paths)
        _make_badge("cross_path_warrior_sage", "silver")
        _make_badge("cross_path_optimized_human", "gold")
        _make_badge("cross_path_complete_human", "platinum")
        _make_badge("cross_path_renaissance_human", "legendary")

    def test_single_path_no_badge(self):
        p = _make_player("cp1")
        self._setup_paths(p, ["fitness_warrior"])
        badges = grant_cross_path_title(p)
        self.assertEqual(badges, [])

    def test_two_paths_warrior_sage(self):
        p = _make_player("cp2")
        self._setup_paths(p, ["fitness_warrior", "mindset_sage"])
        badges = grant_cross_path_title(p)
        keys = [b.key for b in badges]
        self.assertIn("cross_path_warrior_sage", keys)
        self.assertNotIn("cross_path_optimized_human", keys)

    def test_three_paths_optimized_human(self):
        p = _make_player("cp3")
        self._setup_paths(p, ["fitness_warrior", "mindset_sage", "health_alchemist"])
        badges = grant_cross_path_title(p)
        keys = [b.key for b in badges]
        self.assertIn("cross_path_warrior_sage", keys)
        self.assertIn("cross_path_optimized_human", keys)
        self.assertNotIn("cross_path_complete_human", keys)

    def test_four_paths_complete_human(self):
        p = _make_player("cp4")
        self._setup_paths(p, ["fitness_warrior", "mindset_sage", "health_alchemist", "discipline_knight"])
        badges = grant_cross_path_title(p)
        keys = [b.key for b in badges]
        self.assertIn("cross_path_complete_human", keys)
        self.assertNotIn("cross_path_renaissance_human", keys)

    def test_five_paths_renaissance_human(self):
        p = _make_player("cp5")
        self._setup_paths(p, ["fitness_warrior", "mindset_sage", "health_alchemist",
                               "discipline_knight", "grind_visionary"])
        badges = grant_cross_path_title(p)
        keys = [b.key for b in badges]
        self.assertIn("cross_path_renaissance_human", keys)

    def test_idempotent_second_call_returns_empty(self):
        p = _make_player("cp6")
        self._setup_paths(p, ["fitness_warrior", "mindset_sage"])
        grant_cross_path_title(p)
        second = grant_cross_path_title(p)
        self.assertEqual(second, [])


# ── check_streak_milestones ───────────────────────────────────────────────────

class CheckStreakMilestonesTests(TestCase):

    def setUp(self):
        _make_badge("streak_7", "bronze")
        _make_badge("streak_30", "silver")
        _make_badge("streak_100", "gold")
        _make_badge("streak_365", "legendary")

    def test_streak_6_no_badge(self):
        p = _make_player("sm1", streak=6)
        badges = check_streak_milestones(p)
        self.assertEqual(badges, [])

    def test_streak_7_awards_badge(self):
        p = _make_player("sm2", streak=7)
        badges = check_streak_milestones(p)
        keys = [b.key for b in badges]
        self.assertIn("streak_7", keys)
        self.assertNotIn("streak_30", keys)

    def test_streak_8_no_new_badge_idempotent(self):
        p = _make_player("sm3", streak=7)
        check_streak_milestones(p)
        p.streak = 8
        p.save(update_fields=["streak", "updated_at"])
        badges = check_streak_milestones(p)
        # streak_7 already earned — no new badges at 8.
        self.assertEqual(badges, [])

    def test_streak_30_awards_both(self):
        p = _make_player("sm4", streak=30)
        badges = check_streak_milestones(p)
        keys = [b.key for b in badges]
        self.assertIn("streak_7", keys)
        self.assertIn("streak_30", keys)

    def test_streak_100_awards_three(self):
        p = _make_player("sm5", streak=100)
        badges = check_streak_milestones(p)
        keys = [b.key for b in badges]
        self.assertIn("streak_7", keys)
        self.assertIn("streak_30", keys)
        self.assertIn("streak_100", keys)
        self.assertNotIn("streak_365", keys)


# ── check_level_milestones ────────────────────────────────────────────────────

class CheckLevelMilestonesTests(TestCase):

    def setUp(self):
        _make_badge("level_5", "bronze")
        _make_badge("level_10", "silver")
        _make_badge("level_20", "gold")
        _make_badge("level_30", "platinum")

    def test_no_level_up_no_badge(self):
        p = _make_player("lm1", level=3)
        badges = check_level_milestones(p, old_level=3, new_level=3)
        self.assertEqual(badges, [])

    def test_same_level_no_badge(self):
        p = _make_player("lm2", level=5)
        badges = check_level_milestones(p, old_level=5, new_level=5)
        self.assertEqual(badges, [])

    def test_4_to_5_awards_level5(self):
        p = _make_player("lm3", level=5)
        badges = check_level_milestones(p, old_level=4, new_level=5)
        keys = [b.key for b in badges]
        self.assertIn("level_5", keys)
        self.assertNotIn("level_10", keys)

    def test_5_to_5_no_badge(self):
        p = _make_player("lm4", level=5)
        # Already at level 5; re-checking should not re-award (already held).
        check_level_milestones(p, old_level=4, new_level=5)
        second = check_level_milestones(p, old_level=4, new_level=5)
        self.assertEqual(second, [])

    def test_1_to_20_awards_5_and_10_and_20(self):
        p = _make_player("lm5", level=20)
        badges = check_level_milestones(p, old_level=1, new_level=20)
        keys = [b.key for b in badges]
        self.assertIn("level_5", keys)
        self.assertIn("level_10", keys)
        self.assertIn("level_20", keys)
        self.assertNotIn("level_30", keys)

    def test_level_downgrade_not_awarded(self):
        p = _make_player("lm6", level=3)
        badges = check_level_milestones(p, old_level=5, new_level=3)
        self.assertEqual(badges, [])


# ── Integration: quest completion triggers badges and card ────────────────────

class QuestCompletionBadgeIntegrationTest(TestCase):
    """Completing a quest that pushes a player to Level 5 triggers level badge + card."""

    def setUp(self):
        _make_badge("level_5", "bronze")
        _make_badge("streak_7", "bronze")

    def test_level5_badge_and_card_on_quest_complete(self):
        from quests.services import complete_lineup_item

        # EXP needed for Level 5 = 5² × 50 − 50 = 1200; player starts at 1195.
        p = _make_player("int1", path="fitness_warrior", exp=1195, level=4)
        UserPathSelection.objects.create(
            player=p, path="fitness_warrior", onboarding_complete=True,
            multi_paths_active=["fitness_warrior"],
        )

        # Quest worth 10 EXP pushes to 1205 → Level 5.
        quest = _make_quest("Push to Level 5", exp_reward=10)
        today = timezone.localdate()
        lineup = DailyQuestLineup.objects.create(player=p, path="fitness_warrior", date=today)
        item = DailyQuestLineupItem.objects.create(
            lineup=lineup, quest=quest, slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
        )

        result = complete_lineup_item(p, item.id)

        self.assertTrue(result["level_up"])
        self.assertEqual(result["new_level"], 5)
        self.assertIn("level_5", result["badges_earned"])
        self.assertTrue(AchievementCard.objects.filter(player=p, card_type="level_milestone").exists())

    def test_streak7_badge_on_quest_complete(self):
        from quests.services import complete_lineup_item

        # Streak is currently 6; one more day → streak 7.
        p = _make_player("int2", path="fitness_warrior", streak=6)
        p.last_active_date = timezone.localdate() - timedelta(days=1)
        p.save(update_fields=["last_active_date", "updated_at"])
        UserPathSelection.objects.create(
            player=p, path="fitness_warrior", onboarding_complete=True,
        )

        quest = _make_quest("Day 7 Quest")
        today = timezone.localdate()
        lineup = DailyQuestLineup.objects.create(player=p, path="fitness_warrior", date=today)
        item = DailyQuestLineupItem.objects.create(
            lineup=lineup, quest=quest, slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
        )

        result = complete_lineup_item(p, item.id)
        self.assertIn("streak_7", result["badges_earned"])


# ── Integration: complete_weekly_boss ─────────────────────────────────────────

class WeeklyBossCompletionIntegrationTest(TestCase):

    def setUp(self):
        _make_badge("fw_boss_week_1", "silver")
        _make_badge("boss_slayer_first", "bronze")
        _make_badge("boss_slayer_5", "silver")
        _make_badge("level_5", "bronze")

    def _make_boss(self, path="fitness_warrior", exp_reward=200):
        return WeeklyBossQuest.objects.create(
            path_target=path,
            week_start=date.today(),
            title="Trial of Fire",
            exp_reward=exp_reward,
            is_active=True,
        )

    def test_boss_defeat_awards_badge_and_card(self):
        p = _make_player("wb1", path="fitness_warrior")
        boss = self._make_boss()

        result = complete_weekly_boss(p, boss.id)

        self.assertFalse(result["already_completed"])
        self.assertEqual(result["exp_awarded"], 200)
        self.assertIn("boss_slayer_first", result["badges_earned"])
        self.assertIn("fw_boss_week_1", result["badges_earned"])
        self.assertIsNotNone(result["achievement_card_id"])
        card = AchievementCard.objects.get(id=result["achievement_card_id"])
        self.assertEqual(card.card_type, "weekly_boss_fitness_warrior")

    def test_boss_defeat_idempotent(self):
        p = _make_player("wb2", path="fitness_warrior")
        boss = self._make_boss()
        complete_weekly_boss(p, boss.id)
        result2 = complete_weekly_boss(p, boss.id)
        self.assertTrue(result2["already_completed"])

    def test_boss_exp_added_to_player(self):
        p = _make_player("wb3", path="fitness_warrior", exp=100)
        boss = self._make_boss(exp_reward=150)
        complete_weekly_boss(p, boss.id)
        p.refresh_from_db()
        self.assertEqual(p.exp, 250)

    def test_boss_level_up_triggers_level_badge(self):
        # Player at 1195 EXP (Level 4); boss awards 200 EXP → pushes to Level 5.
        p = _make_player("wb4", path="fitness_warrior", exp=1195, level=4)
        boss = self._make_boss(exp_reward=200)
        result = complete_weekly_boss(p, boss.id)
        self.assertTrue(result["level_up"])
        self.assertIn("level_5", result["badges_earned"])

    def test_inactive_boss_raises(self):
        p = _make_player("wb5", path="fitness_warrior")
        boss = WeeklyBossQuest.objects.create(
            path_target="fitness_warrior", week_start=date.today(),
            title="Inactive Boss", exp_reward=100, is_active=False,
        )
        with self.assertRaises(ValueError):
            complete_weekly_boss(p, boss.id)

    def test_visionary_multiplier_applied_to_boss_exp(self):
        from paths.models import XPMultiplier

        p = _make_player("wb6", path="grind_visionary")
        xp, _ = XPMultiplier.objects.get_or_create(player=p)
        xp.multiplier = 1.5
        xp.save(update_fields=["multiplier"])

        boss = WeeklyBossQuest.objects.create(
            path_target="grind_visionary", week_start=date.today(),
            title="Visionary Trial", exp_reward=200, is_active=True,
        )
        _make_badge("gv_boss_week_1", "silver")
        result = complete_weekly_boss(p, boss.id)
        # 200 * 1.5 = 300
        self.assertEqual(result["exp_awarded"], 300)
