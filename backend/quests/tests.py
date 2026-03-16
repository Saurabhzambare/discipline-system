from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from quests.models import Quest, QuestCompletion
from quests.services import calculate_level_from_exp, complete_quest


class QuestProgressionServiceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.player = self.user.player

    def test_calculate_level_from_exp_threshold_calculation(self):
        self.assertEqual(calculate_level_from_exp(0), 1)
        self.assertEqual(calculate_level_from_exp(99), 1)
        self.assertEqual(calculate_level_from_exp(100), 2)
        self.assertEqual(calculate_level_from_exp(250), 3)

    def test_complete_quest_awards_exp_and_creates_completion_record(self):
        quest = Quest.objects.create(title="Gym Session", exp_reward=40)

        result = complete_quest(player=self.player, quest=quest)
        self.player.refresh_from_db()

        self.assertEqual(self.player.exp, 40)
        self.assertEqual(self.player.level, 1)
        self.assertEqual(QuestCompletion.objects.filter(player=self.player, quest=quest).count(), 1)
        self.assertEqual(result["exp_gained"], 40)
        self.assertEqual(result["player_exp"], 40)
        self.assertEqual(result["old_level"], 1)
        self.assertEqual(result["new_level"], 1)
        self.assertFalse(result["leveled_up"])

    def test_complete_quest_detects_level_up(self):
        self.player.exp = 90
        self.player.level = 1
        self.player.save(update_fields=["exp", "level"])
        quest = Quest.objects.create(title="Deep Work", exp_reward=15)

        result = complete_quest(player=self.player, quest=quest)
        self.player.refresh_from_db()

        self.assertEqual(self.player.exp, 105)
        self.assertEqual(self.player.level, 2)
        self.assertEqual(result["old_level"], 1)
        self.assertEqual(result["new_level"], 2)
        self.assertTrue(result["leveled_up"])

    def test_complete_quest_prevents_duplicate_same_day_completion(self):
        quest = Quest.objects.create(title="Read 20 Pages", exp_reward=20)

        complete_quest(player=self.player, quest=quest)

        with self.assertRaisesMessage(ValueError, "Quest already completed today."):
            complete_quest(player=self.player, quest=quest)

        self.player.refresh_from_db()
        self.assertEqual(self.player.exp, 20)
        self.assertEqual(QuestCompletion.objects.filter(player=self.player, quest=quest).count(), 1)


class QuestCompletionApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="apiuser",
            password="testpass123",
        )
        self.player = self.user.player
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.complete_url = reverse("quest-complete")

    def test_quest_complete_endpoint_returns_success_progress_payload(self):
        quest = Quest.objects.create(title="Walk", exp_reward=30)

        response = self.client.post(
            self.complete_url,
            {"quest_id": quest.id},
            format="json",
        )

        self.player.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Quest completed successfully.")
        self.assertEqual(response.data["exp_gained"], 30)
        self.assertEqual(response.data["player_exp"], 30)
        self.assertEqual(response.data["old_level"], 1)
        self.assertEqual(response.data["new_level"], 1)
        self.assertFalse(response.data["leveled_up"])
        self.assertEqual(self.player.exp, 30)

    def test_quest_complete_endpoint_rejects_inactive_quest(self):
        inactive_quest = Quest.objects.create(title="Inactive", exp_reward=10, is_active=False)

        response = self.client.post(
            self.complete_url,
            {"quest_id": inactive_quest.id},
            format="json",
        )

        self.player.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Quest not found or inactive.")
        self.assertEqual(self.player.exp, 0)
