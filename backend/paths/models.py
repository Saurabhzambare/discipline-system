from django.db import models

PATH_CHOICES = [
    ("fitness_warrior", "Fitness Warrior"),
    ("mindset_sage", "Mindset Sage"),
    ("health_alchemist", "Health Alchemist"),
    ("discipline_knight", "Discipline Knight"),
    ("grind_visionary", "Grind Visionary"),
]

# ── PATH DISCOVERY ────────────────────────────────────────────────────────────

class PathDiscoveryQuiz(models.Model):
    """
    9-question identity quiz that determines path fit scores.
    Multiple records can exist per player — retakes create new records.
    Previous quiz records are NEVER deleted (see path-discovery.md).
    """
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="path_discovery_quizzes",
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    retake_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        label = f"retake #{self.retake_count}" if self.retake_count else "initial"
        return f"{self.player.user.username} — quiz ({label})"


class QuizAnswer(models.Model):
    """Individual answer record per question within a quiz."""
    quiz = models.ForeignKey(
        PathDiscoveryQuiz,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question_number = models.PositiveSmallIntegerField()  # 1–9
    answer_key = models.CharField(max_length=1)           # A / B / C / D / E

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("quiz", "question_number")]

    def __str__(self):
        return f"Quiz {self.quiz_id} Q{self.question_number}={self.answer_key}"


class PathMatchScore(models.Model):
    """Computed fit score per path after quiz completion."""
    quiz = models.ForeignKey(
        PathDiscoveryQuiz,
        on_delete=models.CASCADE,
        related_name="scores",
    )
    path = models.CharField(max_length=30, choices=PATH_CHOICES)
    raw_score = models.PositiveSmallIntegerField(default=0)
    match_percentage = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Quiz {self.quiz_id} — {self.path}: {self.match_percentage}%"


class UserPathSelection(models.Model):
    """The path(s) the player has committed to."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="path_selection",
    )
    path = models.CharField(max_length=30, choices=PATH_CHOICES)
    committed_at = models.DateTimeField(auto_now_add=True)
    onboarding_complete = models.BooleanField(default=False)
    # Multi-path unlock: additional paths unlocked after 30-day milestones
    multi_paths_active = models.JSONField(default=list)   # e.g. ["fitness_warrior", "mindset_sage"]
    multi_path_unlock_day = models.PositiveSmallIntegerField(default=30)  # day threshold for next unlock

    def __str__(self):
        return f"{self.player.user.username} → {self.path}"


# ── FITNESS WARRIOR ───────────────────────────────────────────────────────────

class SplitDayState(models.Model):
    """Tracks which muscle-group split day the Warrior is currently on."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="split_day_state",
    )
    current_split = models.CharField(max_length=30, default="push")
    last_updated = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.user.username} — split: {self.current_split}"


class FitnessWarriorProfile(models.Model):
    """Persistent onboarding configuration for Fitness Warrior."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="fitness_warrior_profile",
    )
    training_split = models.CharField(max_length=40, default="ppl")
    primary_goal = models.CharField(max_length=40, default="general_performance")
    training_days_per_week = models.PositiveSmallIntegerField(default=4)
    experience_level = models.CharField(max_length=40, default="beginner")
    split_day_start = models.CharField(max_length=20, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.user.username} — fitness profile"


class WisdomLog(models.Model):
    """Daily wisdom/reflection entry for Warrior journaling mechanic."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="wisdom_logs",
    )
    entry = models.TextField()
    log_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "log_date")]
        ordering = ["-log_date"]

    def __str__(self):
        return f"{self.player.user.username} — wisdom {self.log_date}"


# ── MINDSET SAGE ──────────────────────────────────────────────────────────────

class FreedomDayToken(models.Model):
    """One token = one earned rest day the Sage can cash in."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="freedom_tokens",
    )
    earned_on = models.DateField()
    used_on = models.DateField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["earned_on"]

    def __str__(self):
        status = "used" if self.is_used else "available"
        return f"{self.player.user.username} — freedom token ({status})"


class MindsetSageProfile(models.Model):
    """Persistent onboarding configuration for Mindset Sage."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="mindset_sage_profile",
    )
    motivation = models.CharField(max_length=60, default="personal_growth")
    daily_time_commitment = models.CharField(max_length=40, default="30_minutes")
    experience_level = models.CharField(max_length=40, default="complete_beginner")
    archetype = models.CharField(max_length=40, default="warrior_sage")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.user.username} — mindset profile"


# ── HEALTH ALCHEMIST ──────────────────────────────────────────────────────────

class BodyJournal(models.Model):
    """Daily body metrics log for the Alchemist."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="body_journals",
    )
    log_date = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    energy_level = models.PositiveSmallIntegerField(null=True, blank=True)  # 1–10
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "log_date")]
        ordering = ["-log_date"]

    def __str__(self):
        return f"{self.player.user.username} — body journal {self.log_date}"


class ElixirProgress(models.Model):
    """Tracks the Alchemist's elixir-crafting progression."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="elixir_progress",
    )
    elixir_level = models.PositiveSmallIntegerField(default=1)
    current_formula = models.CharField(max_length=100, blank=True, default="")
    brews_completed = models.PositiveIntegerField(default=0)
    last_brew_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.user.username} — elixir lv{self.elixir_level}"


class EquipmentProfile(models.Model):
    """Equipment available to a player — used for quest filtering."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="equipment_profile",
    )
    equipment_list = models.JSONField(default=list)  # ["barbell", "resistance_band", ...]

    def __str__(self):
        return f"{self.player.user.username} — equipment profile"


class QuestChain(models.Model):
    """
    Directed quest dependency edge for chain-based progression.
    parent_quest must be completed before child_quest unlocks.
    """
    parent_quest = models.ForeignKey(
        "quests.Quest",
        on_delete=models.CASCADE,
        related_name="chain_children",
    )
    child_quest = models.ForeignKey(
        "quests.Quest",
        on_delete=models.CASCADE,
        related_name="chain_parents",
    )
    sequence_order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = [("parent_quest", "child_quest")]
        ordering = ["sequence_order", "id"]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(parent_quest=models.F("child_quest")),
                name="paths_questchain_no_self_reference",
            ),
        ]

    def __str__(self):
        return (
            f"QuestChain({self.parent_quest_id} -> {self.child_quest_id}, "
            f"order={self.sequence_order})"
        )


codex/summarize-project-overview-and-next-steps-gp8267
class HealthAlchemistProfile(models.Model):
    """Persistent onboarding configuration for Health Alchemist."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="health_alchemist_profile",
    )
    primary_health_goal = models.CharField(max_length=60, default="full_body_transformation")
    health_relationship = models.CharField(max_length=60, default="starting_from_scratch")
    focus_area = models.CharField(max_length=40, default="all_of_them")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.user.username} — alchemist profile"

main
# ── DISCIPLINE KNIGHT ─────────────────────────────────────────────────────────

class ArmorPiece(models.Model):
    """Individual armor piece the Knight earns by completing quests."""
    SLOT_CHOICES = [
        ("helmet", "Helmet"),
        ("chest", "Chest"),
        ("gauntlets", "Gauntlets"),
        ("legs", "Legs"),
        ("boots", "Boots"),
        ("shield", "Shield"),
    ]

    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="armor_pieces",
    )
    slot = models.CharField(max_length=20, choices=SLOT_CHOICES)
    name = models.CharField(max_length=100)
    earned_at = models.DateTimeField(auto_now_add=True)
    is_equipped = models.BooleanField(default=True)

    class Meta:
        unique_together = [("player", "slot")]

    def __str__(self):
        return f"{self.player.user.username} — {self.slot}: {self.name}"


class DisciplineCode(models.Model):
    """The Knight's personal code of honor — custom commitments."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="discipline_code",
    )
    code_items = models.JSONField(default=list)  # ["No excuses", "Train daily", ...]
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.user.username} — discipline code"


class DisciplineKnightProfile(models.Model):
    """Persistent onboarding configuration for Discipline Knight."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="discipline_knight_profile",
    )
    routine_level = models.CharField(max_length=60, default="no_routine")
    biggest_challenge = models.CharField(max_length=60, default="all_of_them")
    structure_preference = models.CharField(max_length=60, default="semi_structured")
    time_commitment = models.CharField(max_length=30, default="1_hour")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.user.username} — knight profile"


class GraceToken(models.Model):
    """Allows the Knight to miss one quest without breaking their streak."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="grace_tokens",
    )
    earned_on = models.DateField()
    used_on = models.DateField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["earned_on"]

    def __str__(self):
        status = "used" if self.is_used else "available"
        return f"{self.player.user.username} — grace token ({status})"


class StreakShield(models.Model):
    """Protects the Knight's streak from one failure day."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="streak_shield",
    )
    shields_available = models.PositiveSmallIntegerField(default=0)
    last_earned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.user.username} — {self.shields_available} shield(s)"


class TemptationLog(models.Model):
    """Knight logs temptations resisted — builds willpower XP."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="temptation_logs",
    )
    description = models.TextField()
    log_date = models.DateField()
    resisted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-log_date"]

    def __str__(self):
        outcome = "resisted" if self.resisted else "failed"
        return f"{self.player.user.username} — temptation {outcome} {self.log_date}"


class WarRoomEntry(models.Model):
    """Knight's weekly battle plan and reflection."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="war_room_entries",
    )
    week_start = models.DateField()
    objectives = models.JSONField(default=list)
    reflection = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "week_start")]
        ordering = ["-week_start"]

    def __str__(self):
        return f"{self.player.user.username} — war room {self.week_start}"


# ── GRIND VISIONARY ───────────────────────────────────────────────────────────

class WeeklyReport(models.Model):
    """Visionary's weekly output report — accountability document."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="weekly_reports",
    )
    week_start = models.DateField()
    revenue_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tasks_completed = models.PositiveIntegerField(default=0)
    reflection = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "week_start")]
        ordering = ["-week_start"]

    def __str__(self):
        return f"{self.player.user.username} — weekly report {self.week_start}"


class SingularGoal(models.Model):
    """The Visionary's one obsessive goal at a time."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="singular_goal",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    target_date = models.DateField(null=True, blank=True)
    is_achieved = models.BooleanField(default=False)
    achieved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.user.username} — goal: {self.title}"


class GrindVisionaryProfile(models.Model):
    """Persistent onboarding configuration for Grind Visionary."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="grind_visionary_profile",
    )
    grind_focus = models.CharField(max_length=40, default="coding_and_tech")
    grind_focus_other = models.CharField(max_length=80, blank=True, default="")
    experience_state = models.CharField(max_length=60, default="complete_beginner")
    daily_hours = models.CharField(max_length=30, default="1_hour")
    current_output_state = models.CharField(max_length=80, default="consume_more_than_create")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.user.username} — visionary profile"


class XPMultiplier(models.Model):
    """Active XP multiplier for the Visionary's output quests."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="xp_multiplier",
    )
    multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    expires_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return f"{self.player.user.username} — {self.multiplier}x XP"


class MultiplierProtection(models.Model):
    """Prevents the Visionary's XP multiplier from resetting on a missed day."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="multiplier_protections",
    )
    earned_on = models.DateField()
    used_on = models.DateField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["earned_on"]

    def __str__(self):
        status = "used" if self.is_used else "available"
        return f"{self.player.user.username} — multiplier protection ({status})"


class OutputLog(models.Model):
    """Daily output log for the Visionary — deep work hours, tasks shipped, revenue."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="output_logs",
    )
    log_date = models.DateField()
    deep_work_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    tasks_shipped = models.PositiveSmallIntegerField(default=0)
    revenue_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("player", "log_date")]
        ordering = ["-log_date"]

    def __str__(self):
        return f"{self.player.user.username} — output {self.log_date}"


# ── CROSS-PATH / SHARED ───────────────────────────────────────────────────────

class SkillTree(models.Model):
    """Per-player, per-path skill tree root."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="skill_trees",
    )
    path = models.CharField(max_length=30, choices=PATH_CHOICES)

    class Meta:
        unique_together = [("player", "path")]

    def __str__(self):
        return f"{self.player.user.username} — {self.path} skill tree"


class SkillTreeNode(models.Model):
    """Individual unlockable node in a skill tree."""
    tree = models.ForeignKey(
        SkillTree,
        on_delete=models.CASCADE,
        related_name="nodes",
    )
    node_key = models.CharField(max_length=50)
    is_unlocked = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("tree", "node_key")]

    def __str__(self):
        status = "unlocked" if self.is_unlocked else "locked"
        return f"Tree {self.tree_id} — {self.node_key} ({status})"


class AccountabilityPartner(models.Model):
    """Links two players as mutual accountability partners."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="accountability_sent",
    )
    partner = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="accountability_received",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("player", "partner")]

    def __str__(self):
        return f"{self.player.user.username} ↔ {self.partner.user.username}"


class PostFirstDollarChain(models.Model):
    """Visionary milestone: consecutive days with revenue > $0."""
    player = models.OneToOneField(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="post_first_dollar_chain",
    )
    current_chain = models.PositiveIntegerField(default=0)
    longest_chain = models.PositiveIntegerField(default=0)
    last_revenue_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.user.username} — ${self.current_chain}d chain"


class PathOnboardingProgress(models.Model):
    """Resume-safe onboarding progress per player/path."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="onboarding_progress",
    )
    path = models.CharField(max_length=30, choices=PATH_CHOICES)
    current_step = models.CharField(max_length=40, default="start")
    answers_snapshot = models.JSONField(default=dict)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("player", "path")]

    def __str__(self):
        status = "done" if self.is_completed else "in_progress"
        return f"{self.player.user.username} — onboarding {self.path} ({status})"
