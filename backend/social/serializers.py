"""Serializer layer for social API payloads."""

from rest_framework import serializers

from .models import (
    AccountabilityPartnerRequest,
    ActivityEvent,
    FriendRequest,
    GroupMembership,
    PostComment,
    PostReaction,
    SocialGroup,
    SocialPost,
)


class FriendRequestCreateSerializer(serializers.Serializer):
    to_player_id = serializers.IntegerField(min_value=1)


class FriendRequestSerializer(serializers.ModelSerializer):
    from_player = serializers.SerializerMethodField()
    to_player = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ["id", "from_player", "to_player", "status", "created_at", "responded_at"]

    def _player_payload(self, player):
        return {"id": player.id, "username": player.user.username}

    def get_from_player(self, obj):
        return self._player_payload(obj.from_player)

    def get_to_player(self, obj):
        return self._player_payload(obj.to_player)


class AccountabilityRequestCreateSerializer(serializers.Serializer):
    to_player_id = serializers.IntegerField(min_value=1)


class AccountabilityRequestSerializer(serializers.ModelSerializer):
    from_player = serializers.SerializerMethodField()
    to_player = serializers.SerializerMethodField()

    class Meta:
        model = AccountabilityPartnerRequest
        fields = ["id", "from_player", "to_player", "status", "created_at", "responded_at"]

    def _player_payload(self, player):
        return {"id": player.id, "username": player.user.username}

    def get_from_player(self, obj):
        return self._player_payload(obj.from_player)

    def get_to_player(self, obj):
        return self._player_payload(obj.to_player)


class FriendshipListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class ActivityEventSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()

    class Meta:
        model = ActivityEvent
        fields = ["id", "event_type", "text_snapshot", "created_at", "actor", "related_post_id", "related_group_id"]

    def get_actor(self, obj):
        return {"id": obj.actor.id, "username": obj.actor.user.username}


class PublicProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPost
        fields = ["id", "post_type", "content", "visibility", "group_id", "created_at", "updated_at", "is_edited"]


class PublicProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    level = serializers.IntegerField()
    exp = serializers.IntegerField()
    streak = serializers.IntegerField()
    recent_activity = ActivityEventSerializer(many=True)
    recent_posts = PublicProfilePostSerializer(many=True)
    is_own_profile = serializers.BooleanField(required=False)


class PostCreateSerializer(serializers.Serializer):
    content = serializers.CharField()
    post_type = serializers.ChoiceField(choices=SocialPost.POST_TYPE_CHOICES, default=SocialPost.TYPE_UPDATE)
    visibility = serializers.ChoiceField(choices=SocialPost.VISIBILITY_CHOICES, default=SocialPost.VISIBILITY_PUBLIC)
    group_id = serializers.IntegerField(required=False, allow_null=True)


class PostUpdateSerializer(serializers.Serializer):
    content = serializers.CharField()
    visibility = serializers.ChoiceField(choices=SocialPost.VISIBILITY_CHOICES)


class PostCommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField()


class PostCommentUpdateSerializer(serializers.Serializer):
    content = serializers.CharField()


class PostReactionUpsertSerializer(serializers.Serializer):
    reaction_type = serializers.ChoiceField(choices=PostReaction.REACTION_CHOICES)


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ["id", "author", "content", "created_at", "updated_at", "is_edited"]

    def get_author(self, obj):
        return {"id": obj.author.id, "username": obj.author.user.username}


class PostReactionSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    class Meta:
        model = PostReaction
        fields = ["id", "player", "reaction_type", "created_at", "updated_at"]

    def get_player(self, obj):
        return {"id": obj.player.id, "username": obj.player.user.username}


class SocialPostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = PostCommentSerializer(many=True, read_only=True)
    reactions = PostReactionSerializer(many=True, read_only=True)

    class Meta:
        model = SocialPost
        fields = [
            "id",
            "author",
            "post_type",
            "content",
            "visibility",
            "group_id",
            "created_at",
            "updated_at",
            "is_edited",
            "comments",
            "reactions",
        ]

    def get_author(self, obj):
        return {"id": obj.author.id, "username": obj.author.user.username}


class GroupCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    description = serializers.CharField(required=False, allow_blank=True)
    is_private = serializers.BooleanField(default=False)


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    member_count = serializers.IntegerField(read_only=True)
    is_member = serializers.BooleanField(read_only=True)

    class Meta:
        model = SocialGroup
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "owner",
            "is_private",
            "member_count",
            "is_member",
            "created_at",
            "updated_at",
        ]

    def get_owner(self, obj):
        return {"id": obj.owner.id, "username": obj.owner.user.username}


class GroupMembershipSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    class Meta:
        model = GroupMembership
        fields = ["id", "player", "role", "joined_at"]

    def get_player(self, obj):
        return {"id": obj.player.id, "username": obj.player.user.username}
