from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from quests.models import DailyCompletionSummary, DailyQuestLineup, DailyQuestLineupItem, PlayerDailyQuestAssignment, Quest, QuestCompletion
from paths.models import UserPathSelection
from quests.services import (
    assign_daily_quests,
    calculate_exp_window,
    calculate_level_from_exp,
    calculate_scaled_exp,
    complete_lineup_item,
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
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        UserPathSelection.objects.update_or_create(
            player=self.player,
            defaults={
                "path": "discipline_knight",
                "onboarding_complete": True,
                "multi_paths_active": ["discipline_knight"],
            },
        )

    def test_calculate_level_from_exp_threshold_calculation(self):
        self.assertEqual(calculate_level_from_exp(0), 1)
        self.assertEqual(calculate_level_from_exp(149), 1)
        self.assertEqual(calculate_level_from_exp(150), 2)
        self.assertEqual(calculate_level_from_exp(399), 2)
        self.assertEqual(calculate_level_from_exp(400), 3)

    def test_calculate_exp_window_returns_consistent_progress_fields(self):
        progress = calculate_exp_window(160)
        self.assertEqual(progress["level"], 2)
        self.assertEqual(progress["current_level_floor"], 150)
        self.assertEqual(progress["next_level_floor"], 400)
        self.assertEqual(progress["exp_in_level"], 10)
        self.assertEqual(progress["exp_for_level"], 250)
        self.assertEqual(progress["exp_to_next_level"], 240)

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
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        Quest.objects.create(title="Quest A", exp_reward=10, rank="D", path_target="discipline_knight")
        Quest.objects.create(title="Quest B", exp_reward=20, rank="D", path_target="discipline_knight")

        first_assignments = list(assign_daily_quests(player=self.player))
        second_assignments = list(assign_daily_quests(player=self.player))

        self.assertGreaterEqual(len(first_assignments), 2)
        self.assertGreaterEqual(len(second_assignments), 2)
        self.assertEqual(
            [assignment.id for assignment in first_assignments],
            [assignment.id for assignment in second_assignments],
        )

    def test_assign_daily_quests_respects_player_path_targeting(self):
        self.player.path = "grind_visionary"
        self.player.save(update_fields=["path", "updated_at"])

        Quest.objects.create(title="Global Quest", exp_reward=10, path_target="")
        Quest.objects.create(title="Visionary Quest", exp_reward=10, path_target="grind_visionary")
        Quest.objects.create(title="Fitness Quest", exp_reward=10, path_target="fitness_warrior")

        assignments = assign_daily_quests(player=self.player)
        assigned_titles = {assignment.quest.title for assignment in assignments}

        self.assertNotIn("Fitness Quest", assigned_titles)
        self.assertTrue(assigned_titles.issubset({"Global Quest", "Visionary Quest"}))

    def test_complete_quest_awards_exp_and_marks_assignment_complete(self):
        today = timezone.localdate()
        quest = Quest.objects.create(title="Gym Session", exp_reward=40, difficulty=Quest.DIFFICULTY_MEDIUM, rank="D", path_target="discipline_knight")
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=today)
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )

        result = complete_quest(player=self.player, quest=quest)
        self.player.refresh_from_db()
        self.assertEqual(result["exp_gained"], 40)
        self.assertEqual(self.player.exp, 40)
        self.assertEqual(QuestCompletion.objects.filter(player=self.player, quest=quest).count(), 1)

    def test_complete_quest_requires_today_assignment(self):
        quest = Quest.objects.create(title="Unassigned", exp_reward=20)

        with self.assertRaisesMessage(ValueError, "Quest is not assigned for today."):
            complete_quest(player=self.player, quest=quest)

    def test_complete_quest_prevents_duplicate_same_day_completion(self):
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        quest = Quest.objects.create(title="Read 20 Pages", exp_reward=20, rank="D", path_target="discipline_knight")
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=timezone.localdate())
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )

        first = complete_quest(player=self.player, quest=quest)
        exp_after_first = self.player.exp
        self.assertFalse(first["already_completed"])

        # Idempotent contract (C4-3): duplicate completion returns success
        # with already_completed=true, no EXP gain, no duplicate row.
        second = complete_quest(player=self.player, quest=quest)
        self.assertTrue(second["already_completed"])
        self.assertEqual(second["exp_gained"], 0)
        self.player.refresh_from_db()
        self.assertEqual(self.player.exp, exp_after_first)

    def test_streak_increments_when_completed_yesterday(self):
        self.player.path = "discipline_knight"
        self.player.streak = 3
        self.player.save(update_fields=["path", "streak", "updated_at"])
        yesterday = timezone.localdate() - timedelta(days=1)
        self.player.last_active_date = yesterday
        self.player.save(update_fields=["last_active_date", "updated_at"])

        yesterday_quest = Quest.objects.create(title="Yesterday Quest", exp_reward=10)
        QuestCompletion.objects.create(
            player=self.player,
            quest=yesterday_quest,
            completion_date=yesterday,
        )

        today_quest = Quest.objects.create(title="Today Quest", exp_reward=20, rank="D", path_target="discipline_knight")
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=timezone.localdate())
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=today_quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )
        complete_quest(player=self.player, quest=today_quest)

        self.player.refresh_from_db()
        self.assertEqual(self.player.streak, 4)

    def test_streak_resets_when_day_missed(self):
        self.player.path = "discipline_knight"
        self.player.streak = 5
        self.player.save(update_fields=["path", "streak", "updated_at"])

        quest = Quest.objects.create(title="Comeback Quest", exp_reward=20, rank="D", path_target="discipline_knight")
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=timezone.localdate())
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )
        complete_quest(player=self.player, quest=quest)

        self.player.refresh_from_db()
        self.assertEqual(self.player.streak, 1)

    def test_complete_lineup_item_levels_up_when_threshold_is_crossed(self):
        today = timezone.localdate()
        self.player.path = "discipline_knight"
        self.player.exp = 140
        self.player.level = 1
        self.player.save(update_fields=["path", "exp", "level", "updated_at"])
        quest = Quest.objects.create(title="Threshold Quest", exp_reward=20, path_target="discipline_knight", rank="D")
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=today)
        item = DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )

        result = complete_lineup_item(self.player, item.id)
        self.player.refresh_from_db()

        self.assertTrue(result["level_up"])
        self.assertEqual(result["new_level"], 2)
        self.assertEqual(result["player_exp"], 160)
        self.assertEqual(result["exp_progress"]["exp_to_next_level"], 240)


class QuestCompletionApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="apiuser",
            password="testpass123",
        )
        self.player = self.user.player
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        UserPathSelection.objects.update_or_create(
            player=self.player,
            defaults={
                "path": "discipline_knight",
                "onboarding_complete": True,
                "multi_paths_active": ["discipline_knight"],
            },
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.complete_url = reverse("quest-complete")
        self.list_url = reverse("quest-list")

    def test_quest_list_endpoint_returns_daily_assignments_with_metadata(self):
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        Quest.objects.create(
            title="Hydration",
            exp_reward=20,
            category=Quest.CATEGORY_HEALTH,
            difficulty=Quest.DIFFICULTY_MEDIUM,
            recurrence=Quest.RECURRENCE_DAILY,
            rank="D",
            path_target="discipline_knight",
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        titles = {item["title"] for item in response.data}
        self.assertIn("Hydration", titles)

    def test_quest_complete_endpoint_returns_scaled_reward_payload(self):
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        quest = Quest.objects.create(
            title="Walk",
            exp_reward=30,
            difficulty=Quest.DIFFICULTY_HARD,
            rank="D",
            path_target="discipline_knight",
        )
        today = timezone.localdate()
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=today)
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )

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
        self.assertEqual(response.data["player_streak"], 1)

    def test_quest_complete_endpoint_rejects_unassigned_quest(self):
        quest = Quest.objects.create(title="Needs Assignment", exp_reward=10, path_target="fitness_warrior")

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

    def test_quest_list_shows_done_today_after_completion(self):
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        quest = Quest.objects.create(title="Done Today Quest", exp_reward=25, path_target="discipline_knight", rank="D")
        today = timezone.localdate()
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=today)
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )

        complete_response = self.client.post(self.complete_url, {"quest_id": quest.id}, format="json")
        self.assertEqual(complete_response.status_code, 200)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data[0]["completed_today"])
        self.assertTrue(response.data[0]["assigned_completed_today"])


class Session7ContractApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="session7", password="pass12345")
        self.player = self.user.player
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def _make_lineup(self, target_date):
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=target_date)
        quest = Quest.objects.create(title=f"Q-{target_date}", exp_reward=20, path_target="discipline_knight", rank="D")
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )
        return lineup

    def test_completion_ring_endpoint_returns_contract_shape(self):
        today = timezone.localdate()
        self._make_lineup(today)
        response = self.client.get(reverse("quest-completion-ring"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("completed", response.data)
        self.assertIn("total", response.data)
        self.assertIn("path_breakdown", response.data)

    def test_tomorrow_preview_returns_categories_only(self):
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)
        lineup = DailyQuestLineup.objects.create(player=self.player, path="discipline_knight", date=tomorrow)
        quest = Quest.objects.create(
            title="Should Not Leak",
            description="No title should appear in preview payload",
            exp_reward=15,
            path_target="discipline_knight",
            rank="D",
            category=Quest.CATEGORY_DISCIPLINE,
        )
        DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        )
        response = self.client.get(reverse("quest-tomorrow-preview"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("categories", response.data)
        self.assertNotIn("quests", response.data)
        self.assertEqual(response.data["categories"], [Quest.CATEGORY_DISCIPLINE])

    def test_adaptive_nudge_accept_endpoint_sets_preference(self):
        today = timezone.localdate()
        for offset in range(7):
            day = today - timedelta(days=offset)
            DailyCompletionSummary.objects.create(
                player=self.player,
                summary_date=day,
                path="discipline_knight",
                quests_completed=3,
                quests_total=3,
                total_exp_earned=100,
                bonus_exp_earned=0,
                streak_status="maintained",
                streak_maintained=True,
                cross_path_bonus_earned=False,
            )
        state = self.client.get(reverse("quest-adaptive-nudge"))
        self.assertEqual(state.status_code, 200)
        self.assertTrue(state.data["show_nudge"])
        decide = self.client.post(reverse("quest-adaptive-nudge"), {"decision": "accept"}, format="json")
        self.assertEqual(decide.status_code, 200)
        self.assertTrue(decide.data["enabled"])
