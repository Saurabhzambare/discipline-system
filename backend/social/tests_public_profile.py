"""C3D-1 backend tests for the extended public profile payload."""

from datetime import date, datetime, timezone as dt_timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from paths.models import (
    ArmorPiece,
    ArmorSystem,
    BodyJournal,
    DarkNightEntry,
    DisciplineCode,
    ElixirProgress,
    FitnessWarriorProfile,
    GraceToken,
    GrindVisionaryProfile,
    HealthAlchemistProfile,
    MindsetSageProfile,
    OutputLog,
    SingularGoal,
    SkillTree,
    SkillTreeNode,
    SplitDayState,
    StreakShield,
    TransmutationMilestone,
    UserPathSelection,
    WisdomLog,
    XPMultiplier,
)
from quests.models import Quest, QuestCompletion

from .models import (
    AccountabilityPartnership,
    AchievementCard,
    Badge,
    UserBadge,
)


def _make_user(username):
    return get_user_model().objects.create_user(username=username, password="testpass123")


class PublicProfileExtensionsTests(TestCase):
    def setUp(self):
        self.owner_user = _make_user("c3d1_owner")
        self.viewer_user = _make_user("c3d1_viewer")
        self.client = APIClient()
        self.url_owner = reverse("social-public-profile", args=[self.owner_user.player.id])

    # ── BACKWARD COMPATIBILITY ──────────────────────────────────────────────

    def test_base_fields_remain_unchanged(self):
        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        self.assertEqual(response.status_code, 200)
        for field in ["id", "username", "level", "exp", "streak",
                      "recent_activity", "recent_posts", "is_own_profile"]:
            self.assertIn(field, response.data)

    def test_extension_fields_present(self):
        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        self.assertIn("path_profiles", response.data)
        self.assertIn("badges", response.data)
        self.assertIn("achievement_cards", response.data)

    # ── PATH SELECTION ──────────────────────────────────────────────────────

    def test_player_with_no_path_data_does_not_crash(self):
        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["path_profiles"], [])

    def test_path_profiles_include_only_active_paths(self):
        UserPathSelection.objects.create(
            player=self.owner_user.player,
            path="fitness_warrior",
            multi_paths_active=["fitness_warrior", "mindset_sage"],
        )
        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        keys = [p["path"] for p in response.data["path_profiles"]]
        self.assertEqual(keys, ["fitness_warrior", "mindset_sage"])

    def test_falls_back_to_player_path_when_no_multi_path(self):
        self.owner_user.player.path = "discipline_knight"
        self.owner_user.player.save(update_fields=["path"])
        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        keys = [p["path"] for p in response.data["path_profiles"]]
        self.assertEqual(keys, ["discipline_knight"])

    # ── FITNESS ─────────────────────────────────────────────────────────────

    def test_fitness_path_profile_fields(self):
        FitnessWarriorProfile.objects.create(
            player=self.owner_user.player,
            training_split="ppl",
            primary_goal="strength",
        )
        SplitDayState.objects.create(player=self.owner_user.player, current_split="pull")
        quest = Quest.objects.create(
            title="Push Day", exp_reward=10, path_target="fitness_warrior",
        )
        QuestCompletion.objects.create(
            player=self.owner_user.player, quest=quest, exp_awarded=10,
        )
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="fitness_warrior",
            multi_paths_active=["fitness_warrior"],
        )

        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertEqual(summary["training_split"], "ppl")
        self.assertEqual(summary["primary_goal"], "strength")
        self.assertEqual(summary["current_split"], "pull")
        self.assertEqual(summary["completed_quests"], 1)

    # ── MINDSET PRIVACY ─────────────────────────────────────────────────────

    def test_mindset_profile_does_not_expose_wisdom_entry(self):
        MindsetSageProfile.objects.create(player=self.owner_user.player, archetype="warrior_sage")
        WisdomLog.objects.create(
            player=self.owner_user.player,
            entry="SECRET wisdom entry",
            log_date=date(2026, 5, 1),
        )
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="mindset_sage",
            multi_paths_active=["mindset_sage"],
        )

        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertEqual(summary["wisdom_log_count"], 1)
        # Privacy: dark_night_count is own-only, hidden for other viewers.
        self.assertIsNone(summary["dark_night_count"])
        # No leakage of entry text anywhere in payload.
        self.assertNotIn("SECRET wisdom entry", str(response.data))

    def test_mindset_dark_night_count_visible_to_self(self):
        MindsetSageProfile.objects.create(player=self.owner_user.player)
        DarkNightEntry.objects.create(
            player=self.owner_user.player,
            entry="private struggle text",
            activated_on=date(2026, 4, 1),
        )
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="mindset_sage",
            multi_paths_active=["mindset_sage"],
        )
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.url_owner)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertEqual(summary["dark_night_count"], 1)
        self.assertNotIn("private struggle text", str(response.data))

    # ── HEALTH PRIVACY ──────────────────────────────────────────────────────

    def test_health_profile_hides_body_journal_sensitive_fields(self):
        HealthAlchemistProfile.objects.create(player=self.owner_user.player)
        ElixirProgress.objects.create(
            player=self.owner_user.player, elixir_level=3, brews_completed=12, fill_days=5,
        )
        BodyJournal.objects.create(
            player=self.owner_user.player,
            log_date=date(2026, 5, 1),
            weight_kg=72.5,
            sleep_hours=6.5,
            energy_level=8,
            notes="ate three pancakes — felt sluggish",
        )
        TransmutationMilestone.objects.create(
            player=self.owner_user.player,
            milestone_key="brew_10",
            achieved_on=date(2026, 4, 20),
        )
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="health_alchemist",
            multi_paths_active=["health_alchemist"],
        )

        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertEqual(summary["elixir_level"], 3)
        self.assertEqual(summary["brews_completed"], 12)
        self.assertEqual(summary["fill_days"], 5)
        self.assertEqual(summary["body_journal_count"], 1)
        self.assertEqual(summary["transmutation_milestone_count"], 1)
        self.assertEqual(summary["latest_transmutation"], "brew_10")
        # No sensitive body journal fields leak.
        body = str(response.data)
        for leak in ["72.5", "ate three pancakes", "sluggish", "sleep_hours", "energy_level"]:
            self.assertNotIn(leak, body)

    # ── DISCIPLINE PRIVACY ──────────────────────────────────────────────────

    def test_discipline_code_hidden_for_other_users(self):
        DisciplineCode.objects.create(
            player=self.owner_user.player,
            code_items=["Train daily", "No excuses"],
        )
        ArmorSystem.objects.create(player=self.owner_user.player, total_cracks=2)
        ArmorPiece.objects.create(
            player=self.owner_user.player, slot="helmet", name="Iron Helm",
        )
        StreakShield.objects.create(player=self.owner_user.player, shields_available=1)
        GraceToken.objects.create(
            player=self.owner_user.player, earned_on=date(2026, 5, 1),
        )
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="discipline_knight",
            multi_paths_active=["discipline_knight"],
        )

        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        path_profile = response.data["path_profiles"][0]
        summary = path_profile["summary"]
        self.assertEqual(summary["armor_piece_count"], 1)
        self.assertEqual(summary["total_cracks"], 2)
        self.assertEqual(summary["streak_shields_available"], 1)
        self.assertEqual(summary["grace_token_count"], 1)
        self.assertIsNone(summary["discipline_code"])
        self.assertIn("discipline_code", path_profile["visibility"]["hidden_fields"])
        self.assertNotIn("Train daily", str(response.data))

    def test_discipline_code_visible_for_own_profile(self):
        DisciplineCode.objects.create(
            player=self.owner_user.player,
            code_items=["Train daily", "No excuses"],
        )
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="discipline_knight",
            multi_paths_active=["discipline_knight"],
        )

        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.url_owner)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertEqual(summary["discipline_code"], ["Train daily", "No excuses"])

    # ── GRIND PRIVACY ───────────────────────────────────────────────────────

    def test_grind_singular_goal_hidden_for_other_users(self):
        GrindVisionaryProfile.objects.create(player=self.owner_user.player)
        XPMultiplier.objects.create(player=self.owner_user.player, multiplier=2.5)
        SingularGoal.objects.create(
            player=self.owner_user.player,
            title="Ship MVP by EOY",
            description="confidential strategy",
        )
        OutputLog.objects.create(
            player=self.owner_user.player,
            log_date=date(2026, 5, 1),
            tasks_shipped=2,
            notes="private notes",
            is_public=True,
        )
        OutputLog.objects.create(
            player=self.owner_user.player,
            log_date=date(2026, 5, 2),
            tasks_shipped=1,
            notes="hidden notes",
            is_public=False,
        )
        tree = SkillTree.objects.create(player=self.owner_user.player, path="grind_visionary")
        SkillTreeNode.objects.create(tree=tree, node_key="node_a", is_unlocked=True)
        SkillTreeNode.objects.create(tree=tree, node_key="node_b", is_unlocked=False)

        UserPathSelection.objects.create(
            player=self.owner_user.player, path="grind_visionary",
            multi_paths_active=["grind_visionary"],
        )

        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        path_profile = response.data["path_profiles"][0]
        summary = path_profile["summary"]
        self.assertEqual(summary["xp_multiplier"], 2.5)
        self.assertIsNone(summary["singular_goal"])
        self.assertIn("singular_goal", path_profile["visibility"]["hidden_fields"])
        self.assertEqual(summary["unlocked_skill_nodes"], 1)
        self.assertEqual(summary["total_skill_nodes"], 2)
        self.assertEqual(summary["public_output_log_count"], 1)
        body = str(response.data)
        self.assertNotIn("Ship MVP", body)
        self.assertNotIn("confidential strategy", body)
        self.assertNotIn("private notes", body)
        self.assertNotIn("hidden notes", body)

    def test_grind_singular_goal_visible_to_self(self):
        GrindVisionaryProfile.objects.create(player=self.owner_user.player)
        SingularGoal.objects.create(
            player=self.owner_user.player, title="Ship MVP by EOY",
        )
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="grind_visionary",
            multi_paths_active=["grind_visionary"],
        )
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.url_owner)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertEqual(summary["singular_goal"], "Ship MVP by EOY")

    def test_grind_accountability_partner_flag(self):
        GrindVisionaryProfile.objects.create(player=self.owner_user.player)
        UserPathSelection.objects.create(
            player=self.owner_user.player, path="grind_visionary",
            multi_paths_active=["grind_visionary"],
        )
        partner_user = _make_user("c3d1_partner")
        # Ordered pair constraint: player_one < player_two by id.
        a, b = sorted([self.owner_user.player, partner_user.player], key=lambda p: p.id)
        AccountabilityPartnership.objects.create(player_one=a, player_two=b)
        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertTrue(summary["has_accountability_partner"])

    # ── BADGES ──────────────────────────────────────────────────────────────

    def test_badges_count_reflects_userbadge_count(self):
        b1 = Badge.objects.create(key="streak_7", name="7-Day Streak", tier="bronze")
        b2 = Badge.objects.create(key="boss_slayer", name="Boss Slayer", tier="silver")
        UserBadge.objects.create(player=self.owner_user.player, badge=b1)
        UserBadge.objects.create(player=self.owner_user.player, badge=b2)

        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        self.assertEqual(response.data["badges"]["count"], 2)
        recent_keys = {b["key"] for b in response.data["badges"]["recent"]}
        self.assertEqual(recent_keys, {"streak_7", "boss_slayer"})

    def test_titles_include_only_canonical_title_keys(self):
        title = Badge.objects.create(
            key="title_warrior_sage", name="Warrior-Sage", tier="silver",
        )
        non_title = Badge.objects.create(
            key="title_some_other_thing", name="Bogus Title", tier="silver",
        )
        regular = Badge.objects.create(key="streak_30", name="30-Day Streak", tier="gold")
        UserBadge.objects.create(player=self.owner_user.player, badge=title)
        UserBadge.objects.create(player=self.owner_user.player, badge=non_title)
        UserBadge.objects.create(player=self.owner_user.player, badge=regular)

        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        title_keys = {t["key"] for t in response.data["badges"]["titles"]}
        self.assertEqual(title_keys, {"title_warrior_sage"})
        # Non-canonical title-prefixed badge falls into recent badges, not titles.
        recent_keys = {b["key"] for b in response.data["badges"]["recent"]}
        self.assertIn("title_some_other_thing", recent_keys)
        self.assertIn("streak_30", recent_keys)

    # ── ACHIEVEMENT CARDS ───────────────────────────────────────────────────

    def test_achievement_cards_returns_compact_recent_cards(self):
        for i in range(3):
            AchievementCard.objects.create(
                player=self.owner_user.player,
                title=f"Card {i}",
                subtitle=f"sub {i}",
                card_type="milestone",
                metadata={"sensitive": "should_not_leak_value"},
            )
        self.client.force_authenticate(user=self.viewer_user)
        response = self.client.get(self.url_owner)
        cards = response.data["achievement_cards"]
        self.assertEqual(len(cards), 3)
        sample = cards[0]
        for field in ["id", "title", "subtitle", "card_type", "earned_at"]:
            self.assertIn(field, sample)
        self.assertNotIn("metadata", sample)
        self.assertNotIn("should_not_leak_value", str(response.data))
