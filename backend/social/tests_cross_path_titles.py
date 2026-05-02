"""
Tests for cross-path title automation (C3B — BUILD_ORDER Step 86).

Tests verify:
- grant_cross_path_title() uses exact path combinations, not count-only.
- Wrong combinations do NOT grant titles.
- Idempotency — second call returns empty.
- complete_path_onboarding() hook triggers grant + AchievementCard.
- No duplicate cards on repeated activation.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from paths.models import UserPathSelection
from players.models import Player
from social.achievements import (
    award_badge,
    generate_achievement_card,
    grant_cross_path_title,
)
from social.models import AchievementCard, Badge, UserBadge

User = get_user_model()


def _make_badge(key, tier="silver", name="", description=""):
    """Create a Badge row for testing."""
    return Badge.objects.create(
        key=key,
        name=name or key.replace("_", " ").title(),
        tier=tier,
        description=description or f"Badge for {key}",
    )


def _seed_title_badges():
    """Seed the four cross-path title badges."""
    _make_badge("title_warrior_sage", "silver", "Warrior-Sage", "Fitness Warrior + Mindset Sage")
    _make_badge("title_optimized_human", "silver", "The Optimized Human", "FW + MS + HA")
    _make_badge("title_complete_human", "gold", "The Complete Human", "FW + MS + HA + DK")
    _make_badge("title_renaissance_human", "gold", "The Renaissance Human", "All five paths")


def _make_player(username, path="fitness_warrior"):
    user = User.objects.create_user(username, password="testpass")
    player = Player.objects.get(user=user)
    player.path = path
    player.save(update_fields=["path", "updated_at"])
    return player


def _set_active_paths(player, paths_list):
    """Create or update UserPathSelection with given active paths."""
    UserPathSelection.objects.update_or_create(
        player=player,
        defaults={
            "path": player.path,
            "multi_paths_active": paths_list,
            "onboarding_complete": True,
        },
    )


# ─────────────────────────────────────────────────────────────────────────────
# Unit tests for grant_cross_path_title()
# ─────────────────────────────────────────────────────────────────────────────


class GrantCrossPathTitleTests(TestCase):
    """Unit tests for exact path combination logic."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        _seed_title_badges()

    def test_single_path_no_title(self):
        """Player with only one path active gets no title."""
        player = _make_player("single1", "fitness_warrior")
        _set_active_paths(player, ["fitness_warrior"])
        awarded = grant_cross_path_title(player)
        self.assertEqual(awarded, [])

    def test_warrior_sage_correct_combo(self):
        """FW + MS grants Warrior-Sage."""
        player = _make_player("ws1", "fitness_warrior")
        _set_active_paths(player, ["fitness_warrior", "mindset_sage"])
        awarded = grant_cross_path_title(player)
        keys = [b.key for b in awarded]
        self.assertIn("title_warrior_sage", keys)
        self.assertTrue(
            UserBadge.objects.filter(player=player, badge__key="title_warrior_sage").exists()
        )

    def test_wrong_combo_no_warrior_sage(self):
        """FW + HA does NOT grant Warrior-Sage."""
        player = _make_player("wrong1", "fitness_warrior")
        _set_active_paths(player, ["fitness_warrior", "health_alchemist"])
        awarded = grant_cross_path_title(player)
        keys = [b.key for b in awarded]
        self.assertNotIn("title_warrior_sage", keys)
        self.assertEqual(keys, [])

    def test_wrong_combo_sage_knight(self):
        """MS + DK does NOT grant Warrior-Sage."""
        player = _make_player("wrong2", "mindset_sage")
        _set_active_paths(player, ["mindset_sage", "discipline_knight"])
        awarded = grant_cross_path_title(player)
        self.assertEqual(awarded, [])

    def test_optimized_human_correct_combo(self):
        """FW + MS + HA grants Warrior-Sage AND Optimized Human."""
        player = _make_player("oh1", "fitness_warrior")
        _set_active_paths(player, ["fitness_warrior", "mindset_sage", "health_alchemist"])
        awarded = grant_cross_path_title(player)
        keys = sorted(b.key for b in awarded)
        self.assertIn("title_warrior_sage", keys)
        self.assertIn("title_optimized_human", keys)

    def test_optimized_human_wrong_combo(self):
        """FW + HA + DK does NOT grant Optimized Human (needs MS)."""
        player = _make_player("oh_wrong", "fitness_warrior")
        _set_active_paths(player, ["fitness_warrior", "health_alchemist", "discipline_knight"])
        awarded = grant_cross_path_title(player)
        self.assertEqual(awarded, [])

    def test_complete_human_correct_combo(self):
        """FW + MS + HA + DK grants Complete Human."""
        player = _make_player("ch1", "fitness_warrior")
        _set_active_paths(player, [
            "fitness_warrior", "mindset_sage", "health_alchemist", "discipline_knight"
        ])
        awarded = grant_cross_path_title(player)
        keys = [b.key for b in awarded]
        self.assertIn("title_complete_human", keys)
        self.assertIn("title_optimized_human", keys)
        self.assertIn("title_warrior_sage", keys)

    def test_renaissance_human_all_five(self):
        """All five paths grants The Renaissance Human."""
        player = _make_player("rh1", "fitness_warrior")
        _set_active_paths(player, [
            "fitness_warrior", "mindset_sage", "health_alchemist",
            "discipline_knight", "grind_visionary",
        ])
        awarded = grant_cross_path_title(player)
        keys = [b.key for b in awarded]
        self.assertIn("title_renaissance_human", keys)
        self.assertIn("title_complete_human", keys)
        self.assertIn("title_optimized_human", keys)
        self.assertIn("title_warrior_sage", keys)
        self.assertEqual(len(keys), 4)

    def test_idempotency(self):
        """Second call returns empty list — no duplicate badges."""
        player = _make_player("idem1", "fitness_warrior")
        _set_active_paths(player, ["fitness_warrior", "mindset_sage"])

        first = grant_cross_path_title(player)
        self.assertEqual(len(first), 1)

        second = grant_cross_path_title(player)
        self.assertEqual(second, [])

        # Only one UserBadge row exists.
        count = UserBadge.objects.filter(player=player, badge__key="title_warrior_sage").count()
        self.assertEqual(count, 1)

    def test_no_selection_no_title(self):
        """Player with no UserPathSelection gets no title."""
        player = _make_player("nosel1", "fitness_warrior")
        # Don't create UserPathSelection.
        awarded = grant_cross_path_title(player)
        self.assertEqual(awarded, [])

    def test_player_path_fallback(self):
        """player.path is included even if not in multi_paths_active."""
        player = _make_player("fb1", "fitness_warrior")
        # multi_paths_active only has mindset_sage — player.path adds fitness_warrior.
        _set_active_paths(player, ["mindset_sage"])
        awarded = grant_cross_path_title(player)
        keys = [b.key for b in awarded]
        self.assertIn("title_warrior_sage", keys)


# ─────────────────────────────────────────────────────────────────────────────
# Integration tests for complete_path_onboarding hook
# ─────────────────────────────────────────────────────────────────────────────


class OnboardingTitleHookTests(TestCase):
    """Integration tests verifying complete_path_onboarding triggers title grants."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        _seed_title_badges()

    def _make_onboarded_player(self, username, path, active_paths):
        """Create a player with existing UserPathSelection (pre-onboarding state)."""
        player = _make_player(username, path)
        UserPathSelection.objects.update_or_create(
            player=player,
            defaults={
                "path": path,
                "multi_paths_active": active_paths,
                "onboarding_complete": False,
            },
        )
        return player

    def test_onboarding_triggers_title_grant(self):
        """Completing onboarding with 2 qualifying paths grants title + card."""
        from paths.models import PathOnboardingProgress
        from paths.services import complete_path_onboarding

        player = self._make_onboarded_player(
            "hook1", "fitness_warrior",
            ["fitness_warrior", "mindset_sage"],
        )

        result = complete_path_onboarding(player, "fitness_warrior")

        self.assertTrue(result["completed"])
        self.assertIn("titles_awarded", result)
        self.assertIn("title_warrior_sage", result["titles_awarded"])

        # AchievementCard was created.
        card = AchievementCard.objects.filter(
            player=player, card_type="cross_path_title_title_warrior_sage"
        ).first()
        self.assertIsNotNone(card)
        self.assertEqual(card.metadata["badge_key"], "title_warrior_sage")

    def test_onboarding_no_title_if_single_path(self):
        """Completing onboarding with one path grants no title."""
        from paths.services import complete_path_onboarding

        player = self._make_onboarded_player(
            "hook2", "fitness_warrior",
            ["fitness_warrior"],
        )

        result = complete_path_onboarding(player, "fitness_warrior")

        self.assertTrue(result["completed"])
        self.assertNotIn("titles_awarded", result)
        self.assertEqual(AchievementCard.objects.filter(player=player).count(), 0)

    def test_onboarding_multiple_titles_at_once(self):
        """Completing onboarding with all 5 paths grants all 4 titles + 4 cards."""
        from paths.services import complete_path_onboarding

        player = self._make_onboarded_player(
            "hook3", "fitness_warrior",
            ["fitness_warrior", "mindset_sage", "health_alchemist",
             "discipline_knight", "grind_visionary"],
        )

        result = complete_path_onboarding(player, "fitness_warrior")

        self.assertEqual(len(result["titles_awarded"]), 4)
        self.assertEqual(AchievementCard.objects.filter(player=player).count(), 4)

    def test_onboarding_idempotent_no_duplicate_cards(self):
        """Repeated onboarding completion doesn't duplicate badges or cards."""
        from paths.services import complete_path_onboarding

        player = self._make_onboarded_player(
            "hook4", "fitness_warrior",
            ["fitness_warrior", "mindset_sage"],
        )

        result1 = complete_path_onboarding(player, "fitness_warrior")
        self.assertEqual(len(result1.get("titles_awarded", [])), 1)

        # Second completion — badge already exists, so no new cards.
        result2 = complete_path_onboarding(player, "fitness_warrior")
        self.assertNotIn("titles_awarded", result2)

        # Only 1 card exists.
        self.assertEqual(
            AchievementCard.objects.filter(
                player=player, card_type="cross_path_title_title_warrior_sage"
            ).count(),
            1,
        )
        # Only 1 UserBadge.
        self.assertEqual(
            UserBadge.objects.filter(player=player, badge__key="title_warrior_sage").count(),
            1,
        )
