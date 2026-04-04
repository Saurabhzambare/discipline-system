from django.contrib.auth import get_user_model
from django.test import TestCase

from paths.models import UserPathSelection
from quests.models import DailyQuestLineup, DailyQuestLineupItem, Quest
from quests.services import get_daily_lineup


class Session5LineupReadinessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="session5_user",
            password="testpass123",
        )
        self.player = self.user.player
        self.player.path = "fitness_warrior"
        self.player.save(update_fields=["path", "updated_at"])

        Quest.objects.create(
            title="Universal Hydration",
            description="Hydrate",
            exp_reward=10,
            path_target="",
            universal_daily=True,
            rank="D",
            pillar="body",
        )
        Quest.objects.create(
            title="Complete 20 Pushups",
            description="Starter",
            exp_reward=20,
            path_target="fitness_warrior",
            rank="D",
            pillar="body",
        )
        Quest.objects.create(
            title="Walk 5000 Steps",
            description="Starter",
            exp_reward=20,
            path_target="fitness_warrior",
            rank="D",
            pillar="body",
        )
        Quest.objects.create(
            title="Hit Your Protein Target",
            description="Starter",
            exp_reward=20,
            path_target="fitness_warrior",
            rank="D",
            pillar="body",
        )

    def test_get_daily_lineup_generates_day1_lineup_for_onboarded_player(self):
        UserPathSelection.objects.create(
            player=self.player,
            path="fitness_warrior",
            onboarding_complete=True,
            multi_paths_active=["fitness_warrior"],
        )

        payload = get_daily_lineup(self.player)

        self.assertIn("lineup", payload)
        self.assertIsNotNone(payload["lineup"])
        lineup = DailyQuestLineup.objects.get(player=self.player, path="fitness_warrior")
        reasons = set(lineup.items.values_list("selection_reason", flat=True))
        self.assertIn(DailyQuestLineupItem.REASON_DAY1_STARTER, reasons)
        self.assertIn(DailyQuestLineupItem.REASON_UNIVERSAL, reasons)

    def test_get_daily_lineup_requires_onboarding_completion(self):
        UserPathSelection.objects.create(
            player=self.player,
            path="fitness_warrior",
            onboarding_complete=False,
            multi_paths_active=["fitness_warrior"],
        )

        payload = get_daily_lineup(self.player)

        self.assertIsNone(payload["lineup"])
        self.assertIn("Complete path onboarding", payload["message"])
        self.assertFalse(DailyQuestLineup.objects.filter(player=self.player).exists())
