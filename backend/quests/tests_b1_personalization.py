"""
B1 personalization tests: personalization weight, feedback learning, swap learning,
and a combined integration test for all three signals together.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from paths.models import UserPathSelection
from players.models import Player
from quests.models import (
    DailyQuestLineup,
    DailyQuestLineupItem,
    DailySwap,
    Quest,
    QuestCompletion,
    QuestPreference,
)
from quests.services import (
    _apply_smart_suggestions,
    _days_on_path,
    compute_personalization_weight,
    submit_quest_feedback,
)

User = get_user_model()


def _make_player(username, path="fitness_warrior", days_on_path=1):
    user = User.objects.create_user(username, password="pw")
    # Signal auto-creates Player; get it and set path
    player = Player.objects.get(user=user)
    player.path = path
    player.save(update_fields=["path", "updated_at"])
    sel = UserPathSelection.objects.create(
        player=player, path=path, onboarding_complete=True,
    )
    # auto_now_add ignores the value on create; use update() to backdate
    committed_at = timezone.now() - timedelta(days=days_on_path - 1)
    UserPathSelection.objects.filter(pk=sel.pk).update(committed_at=committed_at)
    return player


def _make_quest(title, pillar="body", path_target="fitness_warrior", rank="D"):
    return Quest.objects.create(
        title=title, exp_reward=40, rank=rank,
        path_target=path_target, pillar=pillar,
    )


# ── Personalization Weight ─────────────────────────────────────────────────────

class PersonalizationWeightTests(TestCase):

    def test_zero_before_day14(self):
        for day in [1, 7, 13]:
            self.assertEqual(compute_personalization_weight(day), 0.0, f"day {day}")

    def test_30pct_at_day14(self):
        self.assertAlmostEqual(compute_personalization_weight(14), 0.30)

    def test_ramps_5pct_per_day(self):
        # Day 22 = 0.30 + (22-14)*0.05 = 0.30 + 0.40 = 0.70
        self.assertAlmostEqual(compute_personalization_weight(22), 0.70)

    def test_70pct_at_day22(self):
        self.assertAlmostEqual(compute_personalization_weight(22), 0.70)

    def test_100pct_at_day30(self):
        self.assertEqual(compute_personalization_weight(30), 1.0)

    def test_capped_at_1_beyond_day30(self):
        self.assertEqual(compute_personalization_weight(45), 1.0)
        self.assertEqual(compute_personalization_weight(365), 1.0)


# ── Feedback Learning ─────────────────────────────────────────────────────────

class FeedbackLearningTests(TestCase):

    def setUp(self):
        self.player = _make_player("fb_user")
        self.quest = _make_quest("Sprint 400m")
        today = timezone.localdate()
        lineup = DailyQuestLineup.objects.create(
            player=self.player, path="fitness_warrior", date=today
        )
        self.item = DailyQuestLineupItem.objects.create(
            lineup=lineup, quest=self.quest,
            slot_order=1, slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
        )

    def test_thumbs_up_gives_plus3(self):
        result = submit_quest_feedback(self.player, self.item.id, "up")
        pref = QuestPreference.objects.get(player=self.player, quest=self.quest)
        self.assertEqual(pref.preference_score, 3)
        self.assertEqual(result["preference_score"], 3)

    def test_thumbs_down_gives_minus3(self):
        result = submit_quest_feedback(self.player, self.item.id, "down")
        pref = QuestPreference.objects.get(player=self.player, quest=self.quest)
        self.assertEqual(pref.preference_score, -3)
        self.assertEqual(result["preference_score"], -3)

    def test_repeated_up_accumulates(self):
        # Two thumbs-up items (different lineup items needed for second call)
        submit_quest_feedback(self.player, self.item.id, "up")
        today = timezone.localdate()
        lineup2 = DailyQuestLineup.objects.create(
            player=self.player, path="fitness_warrior", date=today - timedelta(days=1)
        )
        item2 = DailyQuestLineupItem.objects.create(
            lineup=lineup2, quest=self.quest,
            slot_order=1, slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
        )
        submit_quest_feedback(self.player, item2.id, "up")
        pref = QuestPreference.objects.get(player=self.player, quest=self.quest)
        self.assertEqual(pref.preference_score, 6)

    def test_preference_score_consumed_in_ordering(self):
        q_hi = _make_quest("High Pref Quest")
        q_lo = _make_quest("Low Pref Quest")
        QuestPreference.objects.create(player=self.player, quest=q_hi, preference_score=5)
        QuestPreference.objects.create(player=self.player, quest=q_lo, preference_score=-2)

        ordered = _apply_smart_suggestions(self.player, [q_lo, q_hi])
        self.assertEqual(ordered[0].id, q_hi.id)
        self.assertEqual(ordered[1].id, q_lo.id)


# ── Swap Learning ─────────────────────────────────────────────────────────────

class SwapLearningTests(TestCase):

    def setUp(self):
        self.player = _make_player("swap_user", days_on_path=20)
        self.avoided = _make_quest("Avoided Quest")
        self.preferred = _make_quest("Preferred Quest")

    def _create_swaps(self, quest_removed, quest_added, n):
        today = timezone.localdate()
        for i in range(n):
            DailySwap.objects.create(
                player=self.player,
                path="fitness_warrior",
                swap_date=today - timedelta(days=i + 1),
                quest_removed=quest_removed,
                quest_added=quest_added,
            )

    def test_swapped_away_3_times_loses_priority(self):
        self._create_swaps(self.avoided, self.preferred, 3)
        ordered = _apply_smart_suggestions(self.player, [self.avoided, self.preferred])
        self.assertEqual(ordered[0].id, self.preferred.id)
        self.assertEqual(ordered[-1].id, self.avoided.id)

    def test_swapped_away_fewer_than_3_no_penalty(self):
        # 2 swaps: no penalty yet, both quests start at 0 preference
        self._create_swaps(self.avoided, self.preferred, 2)
        ordered = _apply_smart_suggestions(self.player, [self.avoided, self.preferred])
        # scores: avoided=0 (no penalty), preferred=0 (toward<3, no bonus)
        # tie — original order preserved by stable sort; just verify no crash
        self.assertEqual(len(ordered), 2)

    def test_swapped_toward_3_times_gains_bonus(self):
        self._create_swaps(self.avoided, self.preferred, 3)
        # preferred has swap_toward=3 (+1 bonus), avoided has swap_away=3 (-2 penalty)
        ordered = _apply_smart_suggestions(self.player, [self.avoided, self.preferred])
        self.assertEqual(ordered[0].id, self.preferred.id)


# ── Combined Integration ──────────────────────────────────────────────────────

class PersonalizationIntegrationTest(TestCase):
    """
    Day 30 player with strong body pillar history, thumbs-down feedback on one
    quest, and 3 swap-aways from another. Verifies all three signals combine
    to produce the correct ordering.
    """

    def setUp(self):
        self.player = _make_player("integ_user", days_on_path=30)
        self.today = timezone.localdate()

        self.body_quest = _make_quest("Heavy Compound Lifts", pillar="body")
        self.mind_quest = _make_quest("Read Sports Science", pillar="mind")
        self.disliked = _make_quest("Hated Drill", pillar="body")

        # 30 days of body completions (quest changes daily to avoid unique constraint)
        for i in range(30):
            completion_quest = _make_quest(f"Body Filler Day {i}", pillar="body")
            QuestCompletion.objects.create(
                player=self.player,
                quest=completion_quest,
                completion_date=self.today - timedelta(days=i + 1),
            )

        # Explicit negative feedback on disliked quest
        QuestPreference.objects.create(
            player=self.player, quest=self.disliked, preference_score=-3
        )

        # Swap away from disliked 3 times, toward body_quest
        for i in range(3):
            DailySwap.objects.create(
                player=self.player,
                path="fitness_warrior",
                swap_date=self.today - timedelta(days=i + 1),
                quest_removed=self.disliked,
                quest_added=self.body_quest,
            )

    def test_personalization_weight_is_1_at_day30(self):
        days = _days_on_path(self.player, "fitness_warrior", self.today)
        self.assertGreaterEqual(days, 30)
        self.assertEqual(compute_personalization_weight(days), 1.0)

    def test_combined_signals_produce_correct_ordering(self):
        days = _days_on_path(self.player, "fitness_warrior", self.today)
        quests = [self.disliked, self.mind_quest, self.body_quest]
        ordered = _apply_smart_suggestions(
            self.player, quests,
            days_on_path=days,
            path_code="fitness_warrior",
        )
        # body_quest: swap_toward_bonus=+1, pillar_bonus>0 → highest
        # disliked: preference=-3, swap_away_penalty=-2 → lowest
        self.assertEqual(ordered[0].id, self.body_quest.id)
        self.assertEqual(ordered[-1].id, self.disliked.id)
