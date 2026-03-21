"""Read-only query helpers for social domain."""

from django.db.models import Q

from .models import ActivityEvent, Friendship, GroupMembership, SocialGroup, SocialPost


def friend_ids_for_player(*, player):
    """Return friend player ids for the given player."""
    friendship_qs = Friendship.objects.filter(Q(player_one=player) | Q(player_two=player))
    friend_ids = []
    for friendship in friendship_qs.values("player_one_id", "player_two_id"):
        friend_ids.append(
            friendship["player_two_id"] if friendship["player_one_id"] == player.id else friendship["player_one_id"]
        )
    return friend_ids


def visible_posts_queryset_for_player(*, player):
    """Newest-first posts visible to the player based on simple visibility rules."""
    friend_ids = friend_ids_for_player(player=player)

    return (
        SocialPost.objects.select_related("author__user", "group")
        .prefetch_related("comments__author__user", "reactions__player__user")
        .filter(
            Q(visibility=SocialPost.VISIBILITY_PUBLIC)
            | Q(author=player)
            | Q(visibility=SocialPost.VISIBILITY_FRIENDS_ONLY, author_id__in=friend_ids)
        )
        .order_by("-created_at")
    )


def visible_post_queryset_for_player(*, player, post_id):
    return visible_posts_queryset_for_player(player=player).filter(id=post_id)


def profile_activity_queryset(*, target_player):
    """Public activity events for a player's profile, newest-first."""
    return ActivityEvent.objects.select_related("actor__user", "related_post", "related_group").filter(
        actor=target_player,
        is_public=True,
    ).order_by("-created_at")


def profile_posts_queryset(*, target_player):
    """Recent posts for profile pages, using simple public visibility only."""
    return (
        SocialPost.objects.select_related("author__user", "group")
        .filter(author=target_player, visibility=SocialPost.VISIBILITY_PUBLIC)
        .order_by("-created_at")
    )


def visible_groups_queryset_for_player(*, player):
    """Public groups for everyone + private groups where player is a member."""
    member_group_ids = GroupMembership.objects.filter(player=player).values_list("group_id", flat=True)

    return (
        SocialGroup.objects.select_related("owner__user")
        .filter(Q(is_private=False) | Q(id__in=member_group_ids))
        .distinct()
        .order_by("name")
    )
