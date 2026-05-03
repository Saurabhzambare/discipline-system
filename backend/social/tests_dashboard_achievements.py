"""C3D-3 tests for the dashboard achievement summary endpoint."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import AchievementCard, Badge, UserBadge


def _make_user(username):
    return get_user_model().objects.create_user(username=username, password="testpass123")


class AchievementSummaryTests(TestCase):
    """Tests for GET /api/social/achievements/summary/."""

    def setUp(self):
        self.user = _make_user("ach_user")
        self.client = APIClient()
        self.url = reverse("social-achievement-summary")

    # ── AUTH ─────────────────────────────────────────────────────────────────

    def test_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    # ── EMPTY STATE ─────────────────────────────────────────────────────────

    def test_empty_state_returns_zeros_and_empty_arrays(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["unlocked_count"], 0)
        self.assertEqual(response.data["recent_badges"], [])
        self.assertEqual(response.data["achievement_card_count"], 0)
        self.assertEqual(response.data["recent_cards"], [])

    # ── BADGES ──────────────────────────────────────────────────────────────

    def test_unlocked_count_equals_userbadge_count(self):
        b1 = Badge.objects.create(key="streak_7", name="7-Day Streak", tier="bronze")
        b2 = Badge.objects.create(key="streak_14", name="14-Day Streak", tier="silver")
        b3 = Badge.objects.create(key="boss_slayer", name="Boss Slayer", tier="gold")
        UserBadge.objects.create(player=self.user.player, badge=b1)
        UserBadge.objects.create(player=self.user.player, badge=b2)
        UserBadge.objects.create(player=self.user.player, badge=b3)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["unlocked_count"], 3)

    def test_recent_badges_returns_compact_payload(self):
        badge = Badge.objects.create(key="streak_7", name="7-Day Streak", tier="bronze")
        UserBadge.objects.create(player=self.user.player, badge=badge)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data["recent_badges"]), 1)
        entry = response.data["recent_badges"][0]
        self.assertEqual(entry["key"], "streak_7")
        self.assertEqual(entry["name"], "7-Day Streak")
        self.assertEqual(entry["tier"], "bronze")
        self.assertIn("earned_at", entry)

    def test_recent_badges_capped_at_five(self):
        badges = [
            Badge.objects.create(key=f"b_{i}", name=f"Badge {i}", tier="bronze")
            for i in range(7)
        ]
        for b in badges:
            UserBadge.objects.create(player=self.user.player, badge=b)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["unlocked_count"], 7)
        self.assertEqual(len(response.data["recent_badges"]), 5)

    # ── ACHIEVEMENT CARDS ───────────────────────────────────────────────────

    def test_achievement_card_count_equals_card_count(self):
        for i in range(4):
            AchievementCard.objects.create(
                player=self.user.player,
                title=f"Card {i}",
                card_type="milestone",
            )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["achievement_card_count"], 4)

    def test_recent_cards_returns_compact_payload(self):
        AchievementCard.objects.create(
            player=self.user.player,
            title="Boss Victory",
            subtitle="Defeated the weekly boss",
            card_type="boss",
            metadata={"secret": "should_not_leak"},
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data["recent_cards"]), 1)
        entry = response.data["recent_cards"][0]
        self.assertIn("id", entry)
        self.assertEqual(entry["title"], "Boss Victory")
        self.assertEqual(entry["subtitle"], "Defeated the weekly boss")
        self.assertEqual(entry["card_type"], "boss")
        self.assertIn("earned_at", entry)

    def test_response_does_not_expose_achievement_card_metadata(self):
        AchievementCard.objects.create(
            player=self.user.player,
            title="Card A",
            card_type="milestone",
            metadata={"sensitive_value": "should_never_appear"},
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        body = str(response.data)
        self.assertNotIn("metadata", body)
        self.assertNotIn("sensitive_value", body)
        self.assertNotIn("should_never_appear", body)

    def test_other_player_badges_not_included(self):
        """Ensure badges belonging to another player are not counted."""
        other_user = _make_user("ach_other")
        badge = Badge.objects.create(key="streak_7", name="7-Day Streak", tier="bronze")
        UserBadge.objects.create(player=other_user.player, badge=badge)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["unlocked_count"], 0)
        self.assertEqual(response.data["achievement_card_count"], 0)
