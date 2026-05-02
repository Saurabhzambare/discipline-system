"""Data models for the social domain."""

from django.db import models
from django.db.models import Q, SET_NULL
from django.utils.text import slugify


class FriendRequest(models.Model):
    """Tracks directed friend requests between two players."""

    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DECLINED, "Declined"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    from_player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
    )
    to_player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=~Q(from_player=models.F("to_player")),
                name="social_friend_request_not_self",
            ),
            models.UniqueConstraint(
                fields=["from_player", "to_player"],
                condition=Q(status="pending"),
                name="social_unique_pending_friend_request_directional",
            ),
        ]


class Friendship(models.Model):
    """Stores symmetric friendships using one normalized row per player pair."""

    player_one = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="friendships_as_player_one",
    )
    player_two = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="friendships_as_player_two",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(player_one__lt=models.F("player_two")),
                name="social_friendship_ordered_pair",
            ),
            models.UniqueConstraint(
                fields=["player_one", "player_two"],
                name="social_unique_friendship_pair",
            ),
        ]


class SocialGroup(models.Model):
    """Social group owned by a player."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="owned_social_groups",
    )
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GroupMembership(models.Model):
    """Membership bridge between players and social groups."""

    ROLE_OWNER = "owner"
    ROLE_MEMBER = "member"

    ROLE_CHOICES = [
        (ROLE_OWNER, "Owner"),
        (ROLE_MEMBER, "Member"),
    ]

    group = models.ForeignKey(
        SocialGroup,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="group_memberships",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-joined_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["group", "player"],
                name="social_unique_group_membership",
            )
        ]


class SocialPost(models.Model):
    """User-authored social content."""

    TYPE_UPDATE = "update"
    TYPE_QUEST_COMPLETION = "quest_completion"
    TYPE_ACHIEVEMENT = "achievement"

    POST_TYPE_CHOICES = [
        (TYPE_UPDATE, "Update"),
        (TYPE_QUEST_COMPLETION, "Quest Completion"),
        (TYPE_ACHIEVEMENT, "Achievement"),
    ]

    VISIBILITY_PUBLIC = "public"
    VISIBILITY_FRIENDS_ONLY = "friends_only"

    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, "Public"),
        (VISIBILITY_FRIENDS_ONLY, "Friends Only"),
    ]

    author = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="social_posts",
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default=TYPE_UPDATE)
    content = models.TextField()
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default=VISIBILITY_PUBLIC)
    group = models.ForeignKey(
        SocialGroup,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]


class PostComment(models.Model):
    """Comments attached to social posts."""

    post = models.ForeignKey(
        SocialPost,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="post_comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]


class PostReaction(models.Model):
    """One reaction per user per post."""

    TYPE_LIKE = "like"
    TYPE_FIRE = "fire"
    TYPE_RESPECT = "respect"
    TYPE_CLAP = "clap"

    REACTION_CHOICES = [
        (TYPE_LIKE, "Like"),
        (TYPE_FIRE, "Fire"),
        (TYPE_RESPECT, "Respect"),
        (TYPE_CLAP, "Clap"),
    ]

    post = models.ForeignKey(
        SocialPost,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="post_reactions",
    )
    reaction_type = models.CharField(max_length=12, choices=REACTION_CHOICES, default=TYPE_LIKE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["post", "player"],
                name="social_unique_post_reaction_per_user",
            )
        ]


class ActivityEvent(models.Model):
    """Snapshot events used for profile activity feeds."""

    TYPE_POST_CREATED = "post_created"
    TYPE_FRIEND_ADDED = "friend_added"
    TYPE_JOINED_GROUP = "joined_group"
    TYPE_QUEST_COMPLETED = "quest_completed"
    TYPE_LEVEL_UP = "level_up"
    TYPE_MULTIPLIER_UPGRADE = "multiplier_upgrade"
    TYPE_STREAK_MILESTONE = "streak_milestone"
    TYPE_BADGE_EARNED = "badge_earned"
    TYPE_CROSS_PATH_TITLE_EARNED = "cross_path_title_earned"
    TYPE_PARTNER_QUEST_COMPLETED = "partner_quest_completed"
    TYPE_PARTNER_LEVEL_UP = "partner_level_up"
    TYPE_FIRST_DOLLAR = "first_dollar"
    TYPE_WEEKLY_BOSS_DEFEATED = "weekly_boss_defeated"

    EVENT_CHOICES = [
        (TYPE_POST_CREATED, "Post Created"),
        (TYPE_FRIEND_ADDED, "Friend Added"),
        (TYPE_JOINED_GROUP, "Joined Group"),
        (TYPE_QUEST_COMPLETED, "Quest Completed"),
        (TYPE_LEVEL_UP, "Level Up"),
        (TYPE_MULTIPLIER_UPGRADE, "Multiplier Upgrade"),
        (TYPE_STREAK_MILESTONE, "Streak Milestone"),
        (TYPE_BADGE_EARNED, "Badge Earned"),
        (TYPE_CROSS_PATH_TITLE_EARNED, "Cross-Path Title Earned"),
        (TYPE_PARTNER_QUEST_COMPLETED, "Partner Quest Completed"),
        (TYPE_PARTNER_LEVEL_UP, "Partner Level Up"),
        (TYPE_FIRST_DOLLAR, "First Dollar"),
        (TYPE_WEEKLY_BOSS_DEFEATED, "Weekly Boss Defeated"),
    ]

    actor = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="activity_events",
    )
    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES)
    text_snapshot = models.CharField(max_length=255, blank=True)
    related_post = models.ForeignKey(
        SocialPost,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_events",
    )
    related_player = models.ForeignKey(
        "players.Player",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_activity_events",
    )
    related_group = models.ForeignKey(
        SocialGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_events",
    )
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class ActivityEventRead(models.Model):
    """Per-player read state for an ActivityEvent.

    ActivityEvent is shared/public feed data, so a per-user read row keeps
    seen state isolated between players.
    """

    event = models.ForeignKey(
        ActivityEvent,
        on_delete=models.CASCADE,
        related_name="reads",
    )
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="activity_event_reads",
    )
    seen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "player"],
                name="social_activity_event_read_unique",
            ),
        ]


class AccountabilityPartnerRequest(models.Model):
    """Narrow accountability invite flow for Grind Visionary mechanics."""

    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    from_player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="sent_accountability_requests",
    )
    to_player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="received_accountability_requests",
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(from_player=models.F("to_player")),
                name="social_accountability_request_not_self",
            ),
            models.UniqueConstraint(
                fields=["from_player", "to_player"],
                condition=Q(status="pending"),
                name="social_unique_pending_accountability_request_directional",
            ),
        ]
        ordering = ["-created_at"]


class AccountabilityPartnership(models.Model):
    """Accepted accountability relationship used by Grind Visionary."""

    player_one = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="accountability_as_player_one",
    )
    player_two = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="accountability_as_player_two",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(player_one__lt=models.F("player_two")),
                name="social_accountability_ordered_pair",
            ),
            models.UniqueConstraint(
                fields=["player_one", "player_two"],
                name="social_unique_accountability_pair",
            ),
        ]
        ordering = ["-created_at"]


# ── BADGES & ACHIEVEMENTS ─────────────────────────────────────────────────────

class Badge(models.Model):
    """
    Global badge definition. Badges are earned by completing specific milestones
    (streaks, boss quests, path achievements, etc.).
    """
    TIER_CHOICES = [
        ("bronze", "Bronze"),
        ("silver", "Silver"),
        ("gold", "Gold"),
        ("platinum", "Platinum"),
        ("legendary", "Legendary"),
    ]

    key = models.CharField(max_length=50, unique=True)  # e.g. "streak_7", "boss_slayer"
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="bronze")
    path_specific = models.CharField(max_length=30, blank=True, default="")  # "" = global
    icon_name = models.CharField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.tier.upper()}] {self.name}"


class UserBadge(models.Model):
    """Player's earned badge instance."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="badges",
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="earners",
    )
    earned_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)  # shown on profile card

    class Meta:
        unique_together = [("player", "badge")]
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.player.user.username} — {self.badge.name}"


class AchievementCard(models.Model):
    """
    Visual achievement card displayed on the player's profile.
    Distinct from badges — cards have richer narrative context.
    """
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="achievement_cards",
    )
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, blank=True, default="")
    earned_at = models.DateTimeField(auto_now_add=True)
    card_type = models.CharField(max_length=30, blank=True, default="")  # e.g. "milestone", "boss"
    metadata = models.JSONField(default=dict)  # flexible payload

    class Meta:
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.player.user.username} — {self.title}"


# ── WEEKLY BOSS ───────────────────────────────────────────────────────────────

class WeeklyBossQuest(models.Model):
    """
    Global weekly boss quest definition. One boss is active per week.
    All players on a given path face the same boss.
    """
    path_target = models.CharField(max_length=30, blank=True, default="")  # "" = all paths
    week_start = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    exp_reward = models.PositiveIntegerField(default=500)
    badge = models.ForeignKey(
        Badge,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="boss_quests",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("path_target", "week_start")]
        ordering = ["-week_start"]

    def __str__(self):
        return f"Boss [{self.week_start}] {self.title}"


class WeeklyBossCompletion(models.Model):
    """Records a player defeating the weekly boss."""
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
        related_name="boss_completions",
    )
    boss = models.ForeignKey(
        WeeklyBossQuest,
        on_delete=models.CASCADE,
        related_name="completions",
    )
    completed_at = models.DateTimeField(auto_now_add=True)
    exp_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("player", "boss")]
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.player.user.username} defeated {self.boss.title}"
