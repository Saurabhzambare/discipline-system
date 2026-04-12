from django.db import models
from django.db.models import SET_NULL
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
        ("fitness_warrior", "Fitness Warrior"),
        ("mindset_sage", "Mindset Sage"),
        ("health_alchemist", "Health Alchemist"),
        ("discipline_knight", "Discipline Knight"),
        ("grind_visionary", "Grind Visionary"),
    ]

    RANK_CHOICES = [
        ("E", "E"), ("D", "D"), ("C", "C"),
        ("B", "B"), ("A", "A"), ("S", "S"),
    ]

    PILLAR_CHOICES = [
        ("body", "Body"),
        ("mind", "Mind"),
        ("soul", "Soul"),
        ("output", "Output"),
    ]

    path_target = models.CharField(max_length=30, choices=PATH_TARGET_CHOICES, blank=True, default="")
    rank = models.CharField(max_length=10, choices=RANK_CHOICES, default="E")
    pillar = models.CharField(max_length=20, choices=PILLAR_CHOICES, default="body")
    pack_id = models.CharField(max_length=50, blank=True, default="")
    cooldown_days = models.PositiveSmallIntegerField(default=0)
    universal_daily = models.BooleanField(default=False)
    is_rest_day_quest = models.BooleanField(default=False)
    is_weekly_boss = models.BooleanField(default=False)
    is_one_time_only = models.BooleanField(default=False)
    equipment_required = models.CharField(max_length=100, blank=True, default="")

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


# ── DAILY QUEST LINEUP ────────────────────────────────────────────────────────

class DailyQuestLineup(models.Model):
    """One generated lineup per player/path/date."""
    INTENTION_FULL_SEND = "full_send"
    INTENTION_STEADY = "steady"
    INTENTION_RECOVERY = "recovery"
    INTENTION_CHOICES = [
        (INTENTION_FULL_SEND, "Full Send"),
        (INTENTION_STEADY, "Steady"),
        (INTENTION_RECOVERY, "Recovery"),
    ]

    PATH_CHOICES = [
        ("fitness_warrior", "Fitness Warrior"),
        ("mindset_sage", "Mindset Sage"),
        ("health_alchemist", "Health Alchemist"),
        ("discipline_knight", "Discipline Knight"),
        ("grind_visionary", "Grind Visionary"),
    ]

    player = models.ForeignKey("players.Player", on_delete=models.CASCADE, related_name="daily_lineups")
    path = models.CharField(max_length=30, choices=PATH_CHOICES, default="fitness_warrior")
    date = models.DateField(default=timezone.localdate)
    intention = models.CharField(max_length=20, choices=INTENTION_CHOICES, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["player", "path", "date"], name="unique_daily_lineup_player_path_date"),
        ]
        ordering = ["-date", "path"]

    def __str__(self):
        return f"{self.player.user.username} — {self.path} lineup {self.date}"


class DailyQuestLineupItem(models.Model):
    SLOT_UNIVERSAL = "universal"
    SLOT_ASSIGNED = "assigned"
    SLOT_BONUS = "bonus"
    SLOT_CROSS_PATH = "cross_path"
    SLOT_CHOICES = [
        (SLOT_UNIVERSAL, "Universal"),
        (SLOT_ASSIGNED, "Assigned"),
        (SLOT_BONUS, "Bonus"),
        (SLOT_CROSS_PATH, "Cross Path"),
    ]

    REASON_UNIVERSAL = "universal"
    REASON_PATH_CORE = "path_core"
    REASON_PATH_OVERRIDE = "path_override"
    REASON_WEEKLY_RHYTHM = "weekly_rhythm"
    REASON_SMART_SCORE = "smart_score"
    REASON_CARRY_OVER = "carry_over"
    REASON_CROSS_PATH_BONUS = "cross_path_bonus"
    REASON_FALLBACK = "fallback"
    REASON_DAY1_STARTER = "day1_starter"
    REASON_INTENTION_ADJUSTMENT = "intention_adjustment"
    REASON_CHOICES = [
        (REASON_UNIVERSAL, "Universal"),
        (REASON_PATH_CORE, "Path Core"),
        (REASON_PATH_OVERRIDE, "Path Override"),
        (REASON_WEEKLY_RHYTHM, "Weekly Rhythm"),
        (REASON_SMART_SCORE, "Smart Score"),
        (REASON_CARRY_OVER, "Carry Over"),
        (REASON_CROSS_PATH_BONUS, "Cross Path Bonus"),
        (REASON_FALLBACK, "Fallback"),
        (REASON_DAY1_STARTER, "Day 1 Starter"),
        (REASON_INTENTION_ADJUSTMENT, "Intention Adjustment"),
    ]

    FEEDBACK_CHOICES = [
        ("up", "Thumbs Up"),
        ("down", "Thumbs Down"),
    ]

    lineup = models.ForeignKey(DailyQuestLineup, on_delete=models.CASCADE, related_name="items")
    quest = models.ForeignKey("quests.Quest", on_delete=models.SET_NULL, null=True, blank=True, related_name="lineup_items")
    slot_order = models.PositiveSmallIntegerField()
    slot_type = models.CharField(max_length=20, choices=SLOT_CHOICES, default=SLOT_ASSIGNED)
    is_locked = models.BooleanField(default=False)
    is_carried_over = models.BooleanField(default=False)
    selection_reason = models.CharField(max_length=30, choices=REASON_CHOICES, default=REASON_PATH_CORE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    swapped_from_quest = models.ForeignKey(
        "quests.Quest",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="swapped_from_lineup_items",
    )
    feedback = models.CharField(max_length=4, choices=FEEDBACK_CHOICES, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lineup", "slot_order"], name="unique_lineup_slot_order"),
        ]
        ordering = ["slot_order", "id"]

    def __str__(self):
        return f"Lineup {self.lineup_id} slot {self.slot_order}"


class QuestFeedback(models.Model):
    """Player thumbs-up/down on a quest — feeds the assignment algorithm."""
    RATING_UP = "up"
    RATING_DOWN = "down"
    RATING_CHOICES = [(RATING_UP, "Up"), (RATING_DOWN, "Down")]

    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="quest_feedback",
    )
    quest = models.ForeignKey(
        "quests.Quest",
        on_delete=models.CASCADE,
        related_name="feedback",
    )
    rating = models.CharField(max_length=4, choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "quest")]

    def __str__(self):
        return f"{self.player.user.username} — {self.quest.title}: {self.rating}"


class QuestPreference(models.Model):
    """Per-player preference weight for a quest — updated from feedback."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="quest_preferences",
    )
    quest = models.ForeignKey(
        "quests.Quest",
        on_delete=models.CASCADE,
        related_name="preferences",
    )
    preference_score = models.IntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)
    last_skipped = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("player", "quest")]

    def __str__(self):
        return f"{self.player.user.username} — {self.quest.title}: {self.preference_score}"


class DailyIntention(models.Model):
    """Player's one-line focus intention for the day."""
    INTENTION_CHOICES = [
        ("full_send", "Full Send"),
        ("steady", "Steady"),
        ("recovery", "Recovery"),
    ]
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="daily_intentions",
    )
    intention_date = models.DateField()
    intention = models.CharField(max_length=20, choices=INTENTION_CHOICES, default="steady")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "intention_date")]
        ordering = ["-intention_date"]

    def __str__(self):
        return f"{self.player.user.username} — intention {self.intention_date}"


class DailySwap(models.Model):
    """
    Records a player swapping one quest out of their lineup for another.
    Players have a limited number of swaps per day.
    """
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="daily_swaps",
    )
    path = models.CharField(max_length=30, blank=True, default="")
    swap_date = models.DateField()
    lineup_item = models.ForeignKey(
        "quests.DailyQuestLineupItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="swap_events",
    )
    quest_removed = models.ForeignKey(
        "quests.Quest",
        on_delete=SET_NULL,
        null=True,
        related_name="swapped_out",
    )
    quest_added = models.ForeignKey(
        "quests.Quest",
        on_delete=SET_NULL,
        null=True,
        related_name="swapped_in",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-swap_date"]

    def __str__(self):
        return f"{self.player.user.username} — swap {self.swap_date}"


class CrossPathBonus(models.Model):
    """
    Bonus XP event triggered when a player completes quests across multiple
    pillars in a single day (cross-path synergy reward).
    """
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="cross_path_bonuses",
    )
    bonus_date = models.DateField()
    bonus_pair_key = models.CharField(max_length=50, default="")
    pillars_completed = models.JSONField(default=list)  # e.g. ["body", "mind"]
    bonus_exp = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "bonus_date")]
        ordering = ["-bonus_date"]

    def __str__(self):
        return f"{self.player.user.username} — cross-path bonus {self.bonus_date}"


class DailyCompletionSummary(models.Model):
    """
    End-of-day snapshot: total EXP earned, quests completed, streak state.
    Written once per player per day by the quest completion service.
    """
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="daily_summaries",
    )
    summary_date = models.DateField()
    lineup = models.ForeignKey(
        "quests.DailyQuestLineup",
        on_delete=models.CASCADE,
        related_name="summaries",
        null=True,
        blank=True,
    )
    path = models.CharField(max_length=30, blank=True, default="")
    quests_completed = models.PositiveSmallIntegerField(default=0)
    quests_total = models.PositiveSmallIntegerField(default=0)
    total_exp_earned = models.PositiveIntegerField(default=0)
    bonus_exp_earned = models.PositiveIntegerField(default=0)
    streak_status = models.CharField(max_length=30, default="maintained")
    streak_maintained = models.BooleanField(default=True)
    cross_path_bonus_earned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "summary_date")]
        ordering = ["-summary_date"]

    def __str__(self):
        return f"{self.player.user.username} — summary {self.summary_date}"


class AdaptiveDifficultyPreference(models.Model):
    """
    Per-player preference for adaptive difficulty nudge.
    If enabled, lineup generation biases toward harder eligible ranks.
    """
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="adaptive_difficulty_preference",
    )
    enabled = models.BooleanField(default=False)
    last_prompted_on = models.DateField(null=True, blank=True)
    last_decision_on = models.DateField(null=True, blank=True)
    decision_source = models.CharField(max_length=20, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        state = "enabled" if self.enabled else "disabled"
        return f"{self.player.user.username} — adaptive difficulty {state}"
