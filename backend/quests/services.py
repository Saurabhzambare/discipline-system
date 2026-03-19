from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import PlayerDailyQuestAssignment, Quest, QuestCompletion

DIFFICULTY_MULTIPLIERS = {
    Quest.DIFFICULTY_EASY: 1.0,
    Quest.DIFFICULTY_MEDIUM: 1.3,
    Quest.DIFFICULTY_HARD: 1.6,
}


def calculate_level_from_exp(exp: int) -> int:
    return (exp // 100) + 1


def calculate_scaled_exp(*, quest: Quest) -> int:
    multiplier = DIFFICULTY_MULTIPLIERS.get(quest.difficulty, 1.0)
    return max(1, int(round(quest.exp_reward * multiplier)))


def is_quest_scheduled_for_date(*, quest: Quest, date) -> bool:
    if quest.recurrence == Quest.RECURRENCE_DAILY:
        return True
    if quest.recurrence == Quest.RECURRENCE_WEEKDAYS:
        return date.weekday() < 5
    if quest.recurrence == Quest.RECURRENCE_WEEKLY:
        return date.weekday() == 0
    return False


def _eligible_quests_queryset(*, player, date):
    path = player.path or ""
    return (
        Quest.objects.filter(is_active=True)
        .filter(path_target__in=["", path] if path else [""])
        .order_by("id")
    )


@transaction.atomic
def assign_daily_quests(*, player, date=None):
    assignment_date = date or timezone.localdate()

    existing_assignments = PlayerDailyQuestAssignment.objects.filter(
        player=player,
        assignment_date=assignment_date,
    ).select_related("quest")
    if existing_assignments.exists():
        return existing_assignments

    eligible_quests = [
        quest
        for quest in _eligible_quests_queryset(player=player, date=assignment_date)
        if is_quest_scheduled_for_date(quest=quest, date=assignment_date)
    ]

    assignments = []
    for quest in eligible_quests:
        assignments.append(
            PlayerDailyQuestAssignment(
                player=player,
                quest=quest,
                assignment_date=assignment_date,
                assigned_exp_reward=calculate_scaled_exp(quest=quest),
            )
        )

    PlayerDailyQuestAssignment.objects.bulk_create(assignments)

    return PlayerDailyQuestAssignment.objects.filter(
        player=player,
        assignment_date=assignment_date,
    ).select_related("quest")


@transaction.atomic
def complete_quest(*, player, quest):
    today = timezone.localdate()

    assignment = (
        PlayerDailyQuestAssignment.objects.select_for_update()
        .filter(player=player, quest=quest, assignment_date=today)
        .first()
    )
    if not assignment:
        raise ValueError("Quest is not assigned for today.")

    if assignment.completed:
        raise ValueError("Quest already completed today.")

    had_completion_today = QuestCompletion.objects.filter(
        player=player,
        completion_date=today,
    ).exists()

    QuestCompletion.objects.create(
        player=player,
        quest=quest,
        completion_date=today,
    )

    assignment.completed = True
    assignment.completed_at = timezone.now()
    assignment.save(update_fields=["completed", "completed_at", "updated_at"])

    old_level = player.level

    player.exp += assignment.assigned_exp_reward
    player.level = calculate_level_from_exp(player.exp)

    if not had_completion_today:
        yesterday = today - timedelta(days=1)
        completed_yesterday = QuestCompletion.objects.filter(
            player=player,
            completion_date=yesterday,
        ).exists()

        if completed_yesterday:
            player.streak += 1
        else:
            player.streak = 1

    player.save()

    return {
        "exp_gained": assignment.assigned_exp_reward,
        "player_exp": player.exp,
        "player_streak": player.streak,
        "old_level": old_level,
        "new_level": player.level,
        "leveled_up": player.level > old_level,
    }
