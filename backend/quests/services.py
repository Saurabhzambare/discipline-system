from django.db import transaction
from django.utils import timezone

from .models import QuestCompletion


def calculate_level_from_exp(exp: int) -> int:
    """
    Convert total EXP into a player level.

    Phase 2 rule:
    - Every 100 EXP = 1 level up
    - Level starts at 1

    Examples:
    0 EXP   -> Level 1
    99 EXP  -> Level 1
    100 EXP -> Level 2
    250 EXP -> Level 3
    """
    return (exp // 100) + 1


@transaction.atomic
def complete_quest(*, player, quest):
    """
    Complete a quest for a player.

    This function handles the core gameplay rules:
    1. Prevent duplicate completion on the same day
    2. Create a QuestCompletion record
    3. Award EXP to the player
    4. Recalculate the player's level
    5. Return updated progress data

    transaction.atomic ensures that all database operations
    succeed together or fail together.
    """

    # Get today's local date
    today = timezone.localdate()

    # Check whether the player already completed this quest today
    already_completed_today = QuestCompletion.objects.filter(
        player=player,
        quest=quest,
        completion_date=today,
    ).exists()

    if already_completed_today:
        raise ValueError("Quest already completed today.")

    # Create a quest completion record
    QuestCompletion.objects.create(
        player=player,
        quest=quest,
        completion_date=today,
    )

    # Store old level so we can compare after EXP update
    old_level = player.level

    # Add quest EXP reward to the player
    player.exp += quest.exp_reward

    # Recalculate level from updated EXP
    player.level = calculate_level_from_exp(player.exp)

    # Save updated player progress
    player.save()

    # Return useful response data for the API
    return {
        "exp_gained": quest.exp_reward,
        "player_exp": player.exp,
        "old_level": old_level,
        "new_level": player.level,
        "leveled_up": player.level > old_level,
    }