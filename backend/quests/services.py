import math
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
    # Quadratic formula: EXP needed to reach level L = L² × 50 − 50.
    # Inverse: max(1, floor(sqrt((exp + 50) / 50)))
    return max(1, int(math.sqrt((exp + 50) / 50)))


def calculate_exp_for_level(level: int) -> int:
    """Total EXP required to reach `level` from zero."""
    return max(0, level * level * 50 - 50)


def calculate_exp_progress(exp: int) -> dict:
    """Return current level, EXP earned into the current level, and EXP needed for next level."""
    level = calculate_level_from_exp(exp)
    current_threshold = calculate_exp_for_level(level)
    next_threshold = calculate_exp_for_level(level + 1)
    return {
        "level": level,
        "exp_into_level": exp - current_threshold,
        "exp_to_next_level": next_threshold - current_threshold,
    }


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


def _eligible_quests_queryset(*, player):
    path = player.path or ""
    # TODO: filter out quests where equipment_required is not in player's EquipmentProfile
    # TODO: filter out quests on cooldown (QuestCompletion within cooldown_days window)
    return (
        Quest.objects.filter(is_active=True)
        .filter(path_target__in=["", path] if path else [""])
        .order_by("id")
    )


@transaction.atomic
def assign_daily_quests(*, player, date=None):
    assignment_date = date or timezone.localdate()

    # Assignments are stable for the day; if they already exist, always reuse them.
    existing_assignments = PlayerDailyQuestAssignment.objects.filter(
        player=player,
        assignment_date=assignment_date,
    ).select_related("quest")
    if existing_assignments.exists():
        return existing_assignments

    # TODO: replace with five-layer assignment algorithm:
    # Layer 1 — universal_daily quests (assigned to all players)
    # Layer 2 — path-specific pillar quests (body / mind / soul / output)
    # Layer 3 — weekly boss (is_weekly_boss, one per week per path)
    # Layer 4 — one-time quests not yet completed by this player
    # Layer 5 — cooldown-respecting fill quests up to lineup cap (5–7)
    eligible_quests = [
        quest
        for quest in _eligible_quests_queryset(player=player)
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

    # ignore_conflicts keeps this idempotent under concurrent "first request of the day"
    # calls. DB uniqueness remains the hard guarantee.
    if assignments:
        PlayerDailyQuestAssignment.objects.bulk_create(assignments, ignore_conflicts=True)

    return PlayerDailyQuestAssignment.objects.filter(
        player=player,
        assignment_date=assignment_date,
    ).select_related("quest")


@transaction.atomic
def complete_quest(*, player, quest):
    today = timezone.localdate()
    now = timezone.now()

    # Lock the assignment row so duplicate completion attempts cannot race.
    assignment = (
        PlayerDailyQuestAssignment.objects.select_for_update()
        .filter(player=player, quest=quest, assignment_date=today)
        .first()
    )
    if not assignment:
        raise ValueError("Quest is not assigned for today.")

    if assignment.completed:
        raise ValueError("Quest already completed today.")

    # Lock player progression state while exp/level/streak are updated.
    locked_player = type(player).objects.select_for_update().get(pk=player.pk)

    had_completion_today = QuestCompletion.objects.filter(
        player=locked_player,
        completion_date=today,
    ).exists()

    QuestCompletion.objects.create(
        player=locked_player,
        quest=quest,
        completion_date=today,
    )

    assignment.completed = True
    assignment.completed_at = now
    assignment.save(update_fields=["completed", "completed_at", "updated_at"])

    old_level = locked_player.level

    locked_player.exp += assignment.assigned_exp_reward
    locked_player.level = calculate_level_from_exp(locked_player.exp)

    if not had_completion_today:
        yesterday = today - timedelta(days=1)
        completed_yesterday = QuestCompletion.objects.filter(
            player=locked_player,
            completion_date=yesterday,
        ).exists()

        if completed_yesterday:
            locked_player.streak += 1
        else:
            locked_player.streak = 1

    locked_player.save(update_fields=["exp", "level", "streak", "updated_at"])

    return {
        "exp_gained": assignment.assigned_exp_reward,
        "player_exp": locked_player.exp,
        "player_streak": locked_player.streak,
        "old_level": old_level,
        "new_level": locked_player.level,
        "leveled_up": locked_player.level > old_level,
    }
