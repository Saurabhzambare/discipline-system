from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from paths.models import UserPathSelection
from quests.models import DailyQuestLineup, DailyQuestLineupItem, Quest, QuestCompletion
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


class Session5LineupCompletionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="session5_complete_user",
            password="testpass123",
        )
        self.player = self.user.player
        self.player.path = "fitness_warrior"
        self.player.save(update_fields=["path", "updated_at"])
        UserPathSelection.objects.create(
            player=self.player,
            path="fitness_warrior",
            onboarding_complete=True,
            multi_paths_active=["fitness_warrior"],
        )
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
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.complete_url = reverse("quest-daily-complete")

    def test_daily_lineup_complete_endpoint_completes_once_and_blocks_duplicate(self):
        payload = get_daily_lineup(self.player)
        lineup_items = payload["lineup"]["items"]
        item_id = next(item["item_id"] for item in lineup_items if item["quest_id"])
        first_response = self.client.post(self.complete_url, {"item_id": item_id}, format="json")

        self.assertEqual(first_response.status_code, 200)
        self.assertTrue(first_response.data["item_completed"])
        self.assertEqual(first_response.data["daily_progress"]["completed"], 1)
        self.assertEqual(QuestCompletion.objects.filter(player=self.player).count(), 1)

        second_response = self.client.post(self.complete_url, {"item_id": item_id}, format="json")
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(second_response.data["detail"], "Quest already completed.")
        self.assertEqual(QuestCompletion.objects.filter(player=self.player).count(), 1)
