from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from paths.models import UserPathSelection
from quests.models import DailyQuestLineup, DailyQuestLineupItem, Quest, QuestCompletion, QuestPreference
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


class Session5InteractionHappyPathTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="session5_interactions_user",
            password="testpass123",
        )
        self.player = self.user.player
        self.player.path = "fitness_warrior"
        self.player.save(update_fields=["path", "updated_at"])

        self.path_selection = UserPathSelection.objects.create(
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
        for title in [
            "Complete 20 Pushups",
            "Walk 5000 Steps",
            "Hit Your Protein Target",
            "Jump Rope 5 Minutes",
            "Do 10 Burpees",
            "Stretch for 10 Minutes",
        ]:
            Quest.objects.create(
                title=title,
                description="Fitness daily",
                exp_reward=20,
                path_target="fitness_warrior",
                rank="D",
                pillar="body",
            )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.lineup_url = reverse("quest-daily")
        self.complete_url = reverse("quest-daily-complete")
        self.swap_alternatives_url = reverse("quest-swap-alternatives")
        self.swap_url = reverse("quest-swap")
        self.intention_url = reverse("quest-intention")
        self.feedback_url = reverse("quest-feedback")
        self.summary_url = reverse("quest-summary")

    def _today_lineup_items(self):
        response = self.client.get(self.lineup_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["lineup"])
        return response.data["lineup"]["items"]

    def _first_assigned_item(self):
        lineup_items = self._today_lineup_items()
        return next(item for item in lineup_items if item["slot_type"] == "assigned" and item["quest_id"])

    def test_swap_happy_path_returns_alternatives_and_updates_lineup(self):
        self.path_selection.committed_at = self.path_selection.committed_at - timezone.timedelta(days=13)
        self.path_selection.save(update_fields=["committed_at"])
        item = self._first_assigned_item()

        alternatives_response = self.client.get(self.swap_alternatives_url, {"item_id": item["item_id"]})
        self.assertEqual(alternatives_response.status_code, 200)
        self.assertTrue(alternatives_response.data["alternatives"])

        new_quest_id = alternatives_response.data["alternatives"][0]["id"]
        swap_response = self.client.post(
            self.swap_url,
            {"item_id": item["item_id"], "new_quest_id": new_quest_id},
            format="json",
        )
        self.assertEqual(swap_response.status_code, 200)
        updated_item = next(lineup_item for lineup_item in swap_response.data["lineup"]["items"] if lineup_item["item_id"] == item["item_id"])
        self.assertEqual(updated_item["quest_id"], new_quest_id)
        self.assertEqual(updated_item["selection_reason"], DailyQuestLineupItem.REASON_PATH_OVERRIDE)

    def test_intention_happy_path_sets_lineup_intention(self):
        lineup = self.client.get(self.lineup_url).data["lineup"]
        response = self.client.post(
            self.intention_url,
            {"date": lineup["date"], "intention": "steady"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["intention_set"], "steady")

        db_lineup = DailyQuestLineup.objects.get(id=lineup["id"])
        self.assertEqual(db_lineup.intention, "steady")

    def test_feedback_happy_path_saves_feedback_and_preference(self):
        item = self._first_assigned_item()
        response = self.client.post(
            self.feedback_url,
            {"item_id": item["item_id"], "feedback": "up"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["saved"])
        self.assertEqual(response.data["feedback"], "up")

        preference = QuestPreference.objects.get(player=self.player, quest_id=item["quest_id"])
        self.assertEqual(preference.preference_score, 1)

    def test_summary_happy_path_returns_daily_completion_summary(self):
        item = self._first_assigned_item()
        complete_response = self.client.post(self.complete_url, {"item_id": item["item_id"]}, format="json")
        self.assertEqual(complete_response.status_code, 200)

        lineup = self.client.get(self.lineup_url).data["lineup"]
        summary_response = self.client.get(self.summary_url, {"date": lineup["date"]})
        self.assertEqual(summary_response.status_code, 200)
        self.assertEqual(summary_response.data["quests_completed"], 1)
        self.assertGreaterEqual(summary_response.data["quests_total"], 1)
