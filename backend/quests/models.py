from django.db import models
from django.utils import timezone


class Quest(models.Model):
    """Quest templates that can be assigned to players each day."""
    CATEGORY_FITNESS = "fitness"
    CATEGORY_DISCIPLINE = "discipline"
    CATEGORY_PRODUCTIVITY = "productivity"
    CATEGORY_HEALTH = "health"
    CATEGORY_RECOVERY = "recovery"

    CATEGORY_CHOICES = [
        (CATEGORY_FITNESS, "Fitness"),
        (CATEGORY_DISCIPLINE, "Discipline"),
        (CATEGORY_PRODUCTIVITY, "Productivity"),
        (CATEGORY_HEALTH, "Health"),
        (CATEGORY_RECOVERY, "Recovery"),
    ]

    DIFFICULTY_EASY = "easy"
    DIFFICULTY_MEDIUM = "medium"
    DIFFICULTY_HARD = "hard"

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, "Easy"),
        (DIFFICULTY_MEDIUM, "Medium"),
        (DIFFICULTY_HARD, "Hard"),
    ]

    RECURRENCE_DAILY = "daily"
    RECURRENCE_WEEKDAYS = "weekdays"
    RECURRENCE_WEEKLY = "weekly"

    RECURRENCE_CHOICES = [
        (RECURRENCE_DAILY, "Daily"),
        (RECURRENCE_WEEKDAYS, "Weekdays"),
        (RECURRENCE_WEEKLY, "Weekly"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    exp_reward = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_DISCIPLINE)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default=DIFFICULTY_EASY)
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default=RECURRENCE_DAILY)
    # Optional path targeting. Empty means quest is valid for all paths.
    PATH_TARGET_CHOICES = [
        ("", "All Paths"),
        ("runner", "Runner"),
        ("gym", "Gym"),
        ("discipline", "Discipline"),
        ("tournament", "Tournament"),
        ("75_hard", "75 Hard"),
    ]

    path_target = models.CharField(max_length=20, choices=PATH_TARGET_CHOICES, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PlayerDailyQuestAssignment(models.Model):
    """
    Per-player, per-day quest state.

    This is the runtime daily snapshot: assigned reward + completion status.
    """

    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="daily_quest_assignments",
    )
    quest = models.ForeignKey(
        "quests.Quest",
        on_delete=models.CASCADE,
        related_name="daily_assignments",
    )

    assignment_date = models.DateField(default=timezone.localdate)
    assigned_exp_reward = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["player", "quest", "assignment_date"],
                name="unique_player_quest_assignment_per_day",
            )
        ]
        indexes = [
            # Hot path for "give me today's assignments for this player".
            models.Index(fields=["player", "assignment_date"]),
        ]
        ordering = ["quest_id"]

    def __str__(self):
        return f"{self.player.user.username} · {self.assignment_date} · {self.quest.title}"


class QuestCompletion(models.Model):
    """
    Historical completion event log.

    Assignment tracks today's mutable state; this model keeps immutable history.
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
        constraints = [
            models.UniqueConstraint(
                fields=["player", "quest", "completion_date"],
                name="unique_player_quest_completion_per_day",
            )
        ]
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.player.user.username} - {self.quest.title} - {self.completion_date}"
