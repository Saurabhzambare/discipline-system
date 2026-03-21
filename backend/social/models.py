"""Data models for the social domain."""

from django.db import models
from django.db.models import Q
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
                check=~Q(from_player=models.F("to_player")),
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
                check=Q(player_one__lt=models.F("player_two")),
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

    EVENT_CHOICES = [
        (TYPE_POST_CREATED, "Post Created"),
        (TYPE_FRIEND_ADDED, "Friend Added"),
        (TYPE_JOINED_GROUP, "Joined Group"),
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
