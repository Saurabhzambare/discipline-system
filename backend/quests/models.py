from django.db import models
from django.utils import timezone


class Quest(models.Model):
    """
    Reusable quest template.

    Example:
    - Gym Session
    - Outdoor Walk
    - Drink 3L Water

    This is NOT tied to a specific player.
    It defines what the quest is and how much EXP it gives.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    exp_reward = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Human-readable name in Django admin and shell.
        """
        return self.title


class QuestCompletion(models.Model):
    """
    Record of a player completing a quest.

    Example:
    Saurabh completed 'Gym Session' on 2026-03-11.

    We store both:
    - completed_at: exact timestamp
    - completion_date: easier daily filtering and uniqueness checks
    """

    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="quest_completions",
    )
    quest = models.ForeignKey(
        "quests.Quest",
        on_delete=models.CASCADE,
        related_name="completions",
    )

    completed_at = models.DateTimeField(default=timezone.now)
    completion_date = models.DateField(default=timezone.localdate)

    class Meta:
        """
        Prevent the same player from completing the same quest
        more than once on the same date.
        """
        constraints = [
            models.UniqueConstraint(
                fields=["player", "quest", "completion_date"],
                name="unique_player_quest_completion_per_day",
            )
        ]
        ordering = ["-completed_at"]

    def __str__(self):
        """
        Helpful admin/shell display.
        """
        return f"{self.player.user.username} - {self.quest.title} - {self.completion_date}"