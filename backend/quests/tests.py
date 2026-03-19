from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from quests.models import PlayerDailyQuestAssignment, Quest, QuestCompletion
from quests.services import (
    assign_daily_quests,
    calculate_level_from_exp,
    calculate_scaled_exp,
    complete_quest,
    is_quest_scheduled_for_date,
)


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

    def test_calculate_scaled_exp_uses_difficulty_multiplier(self):
        easy = Quest.objects.create(title="Easy", exp_reward=20, difficulty=Quest.DIFFICULTY_EASY)
        medium = Quest.objects.create(title="Medium", exp_reward=20, difficulty=Quest.DIFFICULTY_MEDIUM)
        hard = Quest.objects.create(title="Hard", exp_reward=20, difficulty=Quest.DIFFICULTY_HARD)

        self.assertEqual(calculate_scaled_exp(quest=easy), 20)
        self.assertEqual(calculate_scaled_exp(quest=medium), 26)
        self.assertEqual(calculate_scaled_exp(quest=hard), 32)

    def test_is_quest_scheduled_for_date_recurring_rules(self):
        monday = date(2026, 3, 16)
        saturday = date(2026, 3, 14)

        daily = Quest.objects.create(title="Daily", exp_reward=10, recurrence=Quest.RECURRENCE_DAILY)
        weekdays = Quest.objects.create(
            title="Weekdays",
            exp_reward=10,
            recurrence=Quest.RECURRENCE_WEEKDAYS,
        )
        weekly = Quest.objects.create(title="Weekly", exp_reward=10, recurrence=Quest.RECURRENCE_WEEKLY)

        self.assertTrue(is_quest_scheduled_for_date(quest=daily, date=saturday))
        self.assertTrue(is_quest_scheduled_for_date(quest=weekdays, date=monday))
        self.assertFalse(is_quest_scheduled_for_date(quest=weekdays, date=saturday))
        self.assertTrue(is_quest_scheduled_for_date(quest=weekly, date=monday))

    def test_assign_daily_quests_is_deterministic_for_same_day(self):
        Quest.objects.create(title="Quest A", exp_reward=10)
        Quest.objects.create(title="Quest B", exp_reward=20)

        first_assignments = list(assign_daily_quests(player=self.player))
        second_assignments = list(assign_daily_quests(player=self.player))

        self.assertEqual(len(first_assignments), 2)
        self.assertEqual(len(second_assignments), 2)
        self.assertEqual(
            [assignment.id for assignment in first_assignments],
            [assignment.id for assignment in second_assignments],
        )

    def test_assign_daily_quests_respects_player_path_targeting(self):
        self.player.path = "runner"
        self.player.save(update_fields=["path", "updated_at"])

        Quest.objects.create(title="Global Quest", exp_reward=10, path_target="")
        Quest.objects.create(title="Runner Quest", exp_reward=10, path_target="runner")
        Quest.objects.create(title="Gym Quest", exp_reward=10, path_target="gym")

        assignments = assign_daily_quests(player=self.player)
        assigned_titles = {assignment.quest.title for assignment in assignments}

        self.assertIn("Global Quest", assigned_titles)
        self.assertIn("Runner Quest", assigned_titles)
        self.assertNotIn("Gym Quest", assigned_titles)

    def test_complete_quest_awards_exp_and_marks_assignment_complete(self):
        quest = Quest.objects.create(title="Gym Session", exp_reward=40, difficulty=Quest.DIFFICULTY_MEDIUM)
        assign_daily_quests(player=self.player)

        result = complete_quest(player=self.player, quest=quest)
        self.player.refresh_from_db()
        assignment = PlayerDailyQuestAssignment.objects.get(player=self.player, quest=quest)

        self.assertTrue(assignment.completed)
        self.assertEqual(result["exp_gained"], assignment.assigned_exp_reward)
        self.assertEqual(self.player.exp, assignment.assigned_exp_reward)
        self.assertEqual(QuestCompletion.objects.filter(player=self.player, quest=quest).count(), 1)

    def test_complete_quest_requires_today_assignment(self):
        quest = Quest.objects.create(title="Unassigned", exp_reward=20)

        with self.assertRaisesMessage(ValueError, "Quest is not assigned for today."):
            complete_quest(player=self.player, quest=quest)

    def test_complete_quest_prevents_duplicate_same_day_completion(self):
        quest = Quest.objects.create(title="Read 20 Pages", exp_reward=20)
        assign_daily_quests(player=self.player)

        complete_quest(player=self.player, quest=quest)

        with self.assertRaisesMessage(ValueError, "Quest already completed today."):
            complete_quest(player=self.player, quest=quest)

    def test_streak_increments_when_completed_yesterday(self):
        self.player.streak = 3
        self.player.save(update_fields=["streak"])
        yesterday = timezone.localdate() - timedelta(days=1)

        yesterday_quest = Quest.objects.create(title="Yesterday Quest", exp_reward=10)
        QuestCompletion.objects.create(
            player=self.player,
            quest=yesterday_quest,
            completion_date=yesterday,
        )

        today_quest = Quest.objects.create(title="Today Quest", exp_reward=20)
        assign_daily_quests(player=self.player)
        complete_quest(player=self.player, quest=today_quest)

        self.player.refresh_from_db()
        self.assertEqual(self.player.streak, 4)

    def test_streak_resets_when_day_missed(self):
        self.player.streak = 5
        self.player.save(update_fields=["streak"])

        quest = Quest.objects.create(title="Comeback Quest", exp_reward=20)
        assign_daily_quests(player=self.player)
        complete_quest(player=self.player, quest=quest)

        self.player.refresh_from_db()
        self.assertEqual(self.player.streak, 1)


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
        self.list_url = reverse("quest-list")

    def test_quest_list_endpoint_returns_daily_assignments_with_metadata(self):
        Quest.objects.create(
            title="Hydration",
            exp_reward=20,
            category=Quest.CATEGORY_HEALTH,
            difficulty=Quest.DIFFICULTY_MEDIUM,
            recurrence=Quest.RECURRENCE_DAILY,
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Hydration")
        self.assertEqual(response.data[0]["difficulty"], Quest.DIFFICULTY_MEDIUM)
        self.assertEqual(response.data[0]["assigned_completed_today"], False)

    def test_quest_complete_endpoint_returns_scaled_reward_payload(self):
        quest = Quest.objects.create(
            title="Walk",
            exp_reward=30,
            difficulty=Quest.DIFFICULTY_HARD,
        )

        self.client.get(self.list_url)

        response = self.client.post(
            self.complete_url,
            {"quest_id": quest.id},
            format="json",
        )

        self.player.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Quest completed successfully.")
        self.assertEqual(response.data["exp_gained"], 48)
        self.assertEqual(response.data["player_exp"], 48)
        self.assertEqual(response.data["player_streak"], 1)

    def test_quest_complete_endpoint_rejects_unassigned_quest(self):
        quest = Quest.objects.create(title="Needs Assignment", exp_reward=10, path_target="gym")

        response = self.client.post(
            self.complete_url,
            {"quest_id": quest.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "Quest is not assigned for today.")

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
