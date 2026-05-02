"""Tests for extended GET /api/social/profiles/<identifier>/ payload (Step 87)."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from paths.models import FitnessWarriorProfile, MindsetSageProfile, UserPathSelection
from social.models import AchievementCard, Badge, UserBadge

User = get_user_model()


def _make_player(username, path="fitness_warrior"):
    user = User.objects.create_user(username, password="pw")
    player = user.player
    player.path = path
    player.save(update_fields=["path", "updated_at"])
    return player


def _make_badge(key, tier="bronze"):
    badge, _ = Badge.objects.get_or_create(
        key=key,
        defaults={"name": key, "tier": tier},
    )
    return badge


class PublicProfileExtensionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.player = _make_player("hero")
        self.other_player = _make_player("observer", path="mindset_sage")
        self.url = reverse("social-public-profile", args=["hero"])

    # ── base fields still present ─────────────────────────────────────────

    def test_base_fields_still_returned(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        for field in ("id", "username", "level", "exp", "streak", "recent_activity", "recent_posts"):
            self.assertIn(field, response.data)

    # ── new top-level keys present ────────────────────────────────────────

    def test_new_keys_present_in_response(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("path_profiles", response.data)
        self.assertIn("badges", response.data)
        self.assertIn("achievement_cards", response.data)

    # ── is_own_profile detection ──────────────────────────────────────────

    def test_is_own_profile_true_for_owner(self):
        self.client.force_authenticate(user=self.player.user)
        response = self.client.get(self.url)
        self.assertTrue(response.data["is_own_profile"])

    def test_is_own_profile_false_for_other(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        self.assertFalse(response.data["is_own_profile"])

    # ── path_profiles ──────────────────────────────────────────────────────

    def test_path_profiles_returns_active_path(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        path_profiles = response.data["path_profiles"]
        self.assertEqual(len(path_profiles), 1)
        self.assertEqual(path_profiles[0]["path"], "fitness_warrior")
        self.assertEqual(path_profiles[0]["display_name"], "Fitness Warrior")
        self.assertIn("summary", path_profiles[0])
        self.assertIn("own_only", path_profiles[0])

    def test_path_profile_summary_includes_quests_completed(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        summary = response.data["path_profiles"][0]["summary"]
        self.assertIn("quests_completed", summary)
        self.assertEqual(summary["quests_completed"], 0)

    def test_own_only_empty_for_non_owner(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        own_only = response.data["path_profiles"][0]["own_only"]
        self.assertEqual(own_only, {})

    def test_own_only_populated_for_owner_with_profile(self):
        FitnessWarriorProfile.objects.create(
            player=self.player,
            training_split="ppl",
            primary_goal="strength",
            training_days_per_week=5,
            experience_level="intermediate",
        )
        self.client.force_authenticate(user=self.player.user)
        response = self.client.get(self.url)
        own_only = response.data["path_profiles"][0]["own_only"]
        self.assertEqual(own_only["training_split"], "ppl")
        self.assertEqual(own_only["primary_goal"], "strength")
        self.assertEqual(own_only["training_days_per_week"], 5)
        self.assertEqual(own_only["experience_level"], "intermediate")

    def test_own_only_empty_dict_when_no_path_profile_exists(self):
        self.client.force_authenticate(user=self.player.user)
        response = self.client.get(self.url)
        own_only = response.data["path_profiles"][0]["own_only"]
        self.assertEqual(own_only, {})

    def test_multi_path_shows_all_active_paths(self):
        UserPathSelection.objects.create(
            player=self.player,
            path="fitness_warrior",
            onboarding_complete=True,
            multi_paths_active=["fitness_warrior", "mindset_sage"],
        )
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        paths_returned = {pp["path"] for pp in response.data["path_profiles"]}
        self.assertIn("fitness_warrior", paths_returned)
        self.assertIn("mindset_sage", paths_returned)

    # ── badges ────────────────────────────────────────────────────────────

    def test_badges_structure(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        badges = response.data["badges"]
        self.assertIn("total_count", badges)
        self.assertIn("titles", badges)
        self.assertIn("recent", badges)
        self.assertEqual(badges["total_count"], 0)
        self.assertEqual(badges["titles"], [])
        self.assertEqual(badges["recent"], [])

    def test_badges_total_count(self):
        badge = _make_badge("streak_7")
        UserBadge.objects.create(player=self.player, badge=badge)
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["badges"]["total_count"], 1)

    def test_title_badge_appears_in_titles_not_recent(self):
        badge = _make_badge("title_warrior_sage", tier="gold")
        UserBadge.objects.create(player=self.player, badge=badge)
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        badges = response.data["badges"]
        self.assertEqual(len(badges["titles"]), 1)
        self.assertEqual(badges["titles"][0]["key"], "title_warrior_sage")
        self.assertEqual(len(badges["recent"]), 0)

    def test_non_title_badge_appears_in_recent_not_titles(self):
        badge = _make_badge("streak_30", tier="silver")
        UserBadge.objects.create(player=self.player, badge=badge)
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        badges = response.data["badges"]
        self.assertEqual(len(badges["recent"]), 1)
        self.assertEqual(badges["recent"][0]["key"], "streak_30")
        self.assertEqual(len(badges["titles"]), 0)

    def test_recent_badges_capped_at_five(self):
        for i in range(7):
            b = _make_badge(f"streak_{i * 10 + 7}")
            UserBadge.objects.create(player=self.player, badge=b)
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        self.assertLessEqual(len(response.data["badges"]["recent"]), 5)

    def test_badge_item_fields(self):
        badge = _make_badge("streak_7", tier="bronze")
        UserBadge.objects.create(player=self.player, badge=badge)
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        item = response.data["badges"]["recent"][0]
        for field in ("key", "name", "tier", "earned_at"):
            self.assertIn(field, item)

    # ── achievement_cards ─────────────────────────────────────────────────

    def test_achievement_cards_empty_by_default(self):
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["achievement_cards"], [])

    def test_achievement_cards_returned(self):
        AchievementCard.objects.create(
            player=self.player,
            title="First Boss",
            subtitle="Defeated the weekly boss",
            card_type="weekly_boss_fitness_warrior",
            metadata={"boss_id": 1},
        )
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        cards = response.data["achievement_cards"]
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["title"], "First Boss")
        self.assertEqual(cards[0]["card_type"], "weekly_boss_fitness_warrior")
        self.assertIn("metadata", cards[0])

    def test_achievement_card_fields(self):
        AchievementCard.objects.create(
            player=self.player,
            title="Test Card",
            card_type="test",
        )
        self.client.force_authenticate(user=self.other_player.user)
        response = self.client.get(self.url)
        card = response.data["achievement_cards"][0]
        for field in ("id", "title", "subtitle", "card_type", "earned_at", "metadata"):
            self.assertIn(field, card)

    # ── identifier variants ───────────────────────────────────────────────

    def test_profile_lookup_by_player_id(self):
        self.client.force_authenticate(user=self.other_player.user)
        url = reverse("social-public-profile", args=[str(self.player.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("path_profiles", response.data)

    def test_profile_404_for_unknown_identifier(self):
        self.client.force_authenticate(user=self.other_player.user)
        url = reverse("social-public-profile", args=["nobody_here"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
