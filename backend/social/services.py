"""Business rules for social domain operations."""

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from players.models import Player

from .models import (
    ActivityEvent,
    FriendRequest,
    Friendship,
    GroupMembership,
    PostComment,
    PostReaction,
    SocialGroup,
    SocialPost,
)
from .selectors import friend_ids_for_player


class SocialNotFoundError(Exception):
    """Raised when a requested social resource does not exist."""


def _ordered_player_pair(*, player_a, player_b):
    return (player_a, player_b) if player_a.id < player_b.id else (player_b, player_a)


def _friendship_exists(*, player_a, player_b):
    player_one, player_two = _ordered_player_pair(player_a=player_a, player_b=player_b)
    return Friendship.objects.filter(player_one=player_one, player_two=player_two).exists()


def _is_group_member(*, group, player):
    return GroupMembership.objects.filter(group=group, player=player).exists()


def get_group_or_404(*, group_id):
    try:
        return SocialGroup.objects.get(id=group_id)
    except SocialGroup.DoesNotExist as exc:
        raise SocialNotFoundError("Group not found.") from exc


@transaction.atomic
def send_friend_request(*, from_player, to_player_id):
    if from_player.id == to_player_id:
        raise ValidationError("You cannot send a friend request to yourself.")

    try:
        to_player = Player.objects.get(id=to_player_id)
    except Player.DoesNotExist as exc:
        raise SocialNotFoundError("Target player was not found.") from exc

    if _friendship_exists(player_a=from_player, player_b=to_player):
        raise ValidationError("You are already friends with this player.")

    if FriendRequest.objects.filter(
        from_player=from_player,
        to_player=to_player,
        status=FriendRequest.STATUS_PENDING,
    ).exists():
        raise ValidationError("A pending friend request already exists for this player.")

    if FriendRequest.objects.filter(
        from_player=to_player,
        to_player=from_player,
        status=FriendRequest.STATUS_PENDING,
    ).exists():
        raise ValidationError(
            "This player has already sent you a pending friend request. "
            "Please accept or decline that request instead."
        )

    return FriendRequest.objects.create(from_player=from_player, to_player=to_player)


@transaction.atomic
def accept_friend_request(*, request_id, acting_player):
    friend_request = FriendRequest.objects.select_for_update().filter(id=request_id).first()
    if not friend_request:
        raise SocialNotFoundError("Friend request not found.")

    if friend_request.to_player_id != acting_player.id:
        raise PermissionDenied("You can only accept requests sent to you.")

    if friend_request.status != FriendRequest.STATUS_PENDING:
        raise ValidationError("Only pending friend requests can be accepted.")

    player_one, player_two = _ordered_player_pair(
        player_a=friend_request.from_player,
        player_b=friend_request.to_player,
    )

    friendship, _ = Friendship.objects.get_or_create(player_one=player_one, player_two=player_two)

    friend_request.status = FriendRequest.STATUS_ACCEPTED
    friend_request.responded_at = timezone.now()
    friend_request.save(update_fields=["status", "responded_at"])

    ActivityEvent.objects.create(
        actor=acting_player,
        event_type=ActivityEvent.TYPE_FRIEND_ADDED,
        text_snapshot="Became friends",
        related_player=friend_request.from_player,
        is_public=True,
    )

    return friendship


@transaction.atomic
def decline_friend_request(*, request_id, acting_player):
    friend_request = FriendRequest.objects.select_for_update().filter(id=request_id).first()
    if not friend_request:
        raise SocialNotFoundError("Friend request not found.")

    if friend_request.to_player_id != acting_player.id:
        raise PermissionDenied("You can only decline requests sent to you.")

    if friend_request.status != FriendRequest.STATUS_PENDING:
        raise ValidationError("Only pending friend requests can be declined.")

    friend_request.status = FriendRequest.STATUS_DECLINED
    friend_request.responded_at = timezone.now()
    friend_request.save(update_fields=["status", "responded_at"])
    return friend_request


@transaction.atomic
def cancel_friend_request(*, request_id, acting_player):
    friend_request = FriendRequest.objects.select_for_update().filter(id=request_id).first()
    if not friend_request:
        raise SocialNotFoundError("Friend request not found.")

    if friend_request.from_player_id != acting_player.id:
        raise PermissionDenied("You can only cancel requests you sent.")

    if friend_request.status != FriendRequest.STATUS_PENDING:
        raise ValidationError("Only pending friend requests can be cancelled.")

    friend_request.status = FriendRequest.STATUS_CANCELLED
    friend_request.responded_at = timezone.now()
    friend_request.save(update_fields=["status", "responded_at"])
    return friend_request


@transaction.atomic
def remove_friend(*, acting_player, other_player_id):
    try:
        other_player = Player.objects.get(id=other_player_id)
    except Player.DoesNotExist as exc:
        raise SocialNotFoundError("Player not found.") from exc

    player_one, player_two = _ordered_player_pair(player_a=acting_player, player_b=other_player)
    deleted_count, _ = Friendship.objects.filter(player_one=player_one, player_two=player_two).delete()
    if deleted_count == 0:
        raise ValidationError("You are not friends with this player.")



def list_friends_queryset(*, player):
    return Friendship.objects.select_related(
        "player_one__user",
        "player_two__user",
    ).filter(Q(player_one=player) | Q(player_two=player))



def friend_requests_queryset(*, player, direction=None):
    base_qs = FriendRequest.objects.select_related("from_player__user", "to_player__user")

    if direction == "incoming":
        return base_qs.filter(to_player=player)
    if direction == "outgoing":
        return base_qs.filter(from_player=player)

    return base_qs.filter(Q(from_player=player) | Q(to_player=player))



def get_public_profile_player(*, identifier):
    if str(identifier).isdigit():
        try:
            return Player.objects.select_related("user").get(id=int(identifier))
        except Player.DoesNotExist as exc:
            raise SocialNotFoundError("Player not found.") from exc

    try:
        return Player.objects.select_related("user").get(user__username=identifier)
    except Player.DoesNotExist as exc:
        raise SocialNotFoundError("Player not found.") from exc


@transaction.atomic
def create_post(*, author, content, post_type=SocialPost.TYPE_UPDATE, visibility=SocialPost.VISIBILITY_PUBLIC, group_id=None):
    if visibility not in {SocialPost.VISIBILITY_PUBLIC, SocialPost.VISIBILITY_FRIENDS_ONLY}:
        raise ValidationError("Visibility must be public or friends_only.")

    group = None
    if group_id is not None:
        group = get_group_or_404(group_id=group_id)
        if not _is_group_member(group=group, player=author):
            raise PermissionDenied("You must be a member of the group to post in it.")

    post = SocialPost.objects.create(
        author=author,
        content=content,
        post_type=post_type,
        visibility=visibility,
        group=group,
    )

    ActivityEvent.objects.create(
        actor=author,
        event_type=ActivityEvent.TYPE_POST_CREATED,
        text_snapshot="Created a new post",
        related_post=post,
        related_group=group,
        is_public=(visibility == SocialPost.VISIBILITY_PUBLIC),
    )

    return post


@transaction.atomic
def update_post(*, post, acting_player, content, visibility):
    if post.author_id != acting_player.id:
        raise PermissionDenied("You can only update your own posts.")

    if visibility not in {SocialPost.VISIBILITY_PUBLIC, SocialPost.VISIBILITY_FRIENDS_ONLY}:
        raise ValidationError("Visibility must be public or friends_only.")

    post.content = content
    post.visibility = visibility
    post.is_edited = True
    post.save(update_fields=["content", "visibility", "is_edited", "updated_at"])
    return post


@transaction.atomic
def delete_post(*, post, acting_player):
    if post.author_id != acting_player.id:
        raise PermissionDenied("You can only delete your own posts.")
    post.delete()


@transaction.atomic
def add_comment(*, post, acting_player, content):
    return PostComment.objects.create(post=post, author=acting_player, content=content)


@transaction.atomic
def update_comment(*, comment, acting_player, content):
    if comment.author_id != acting_player.id:
        raise PermissionDenied("You can only edit your own comments.")

    comment.content = content
    comment.is_edited = True
    comment.save(update_fields=["content", "is_edited", "updated_at"])
    return comment


@transaction.atomic
def delete_comment(*, comment, acting_player):
    if comment.author_id != acting_player.id:
        raise PermissionDenied("You can only delete your own comments.")
    comment.delete()


@transaction.atomic
def add_or_update_reaction(*, post, acting_player, reaction_type):
    reaction, created = PostReaction.objects.update_or_create(
        post=post,
        player=acting_player,
        defaults={"reaction_type": reaction_type},
    )
    return reaction, created


@transaction.atomic
def remove_reaction(*, post, acting_player):
    deleted_count, _ = PostReaction.objects.filter(post=post, player=acting_player).delete()
    if deleted_count == 0:
        raise ValidationError("No reaction exists for this post.")


@transaction.atomic
def create_group(*, owner, name, description="", is_private=False):
    group = SocialGroup.objects.create(
        name=name,
        description=description,
        owner=owner,
        is_private=is_private,
    )
    GroupMembership.objects.create(group=group, player=owner, role=GroupMembership.ROLE_OWNER)
    return group


@transaction.atomic
def join_group(*, group, acting_player):
    if _is_group_member(group=group, player=acting_player):
        raise ValidationError("You are already a member of this group.")

    membership = GroupMembership.objects.create(
        group=group,
        player=acting_player,
        role=GroupMembership.ROLE_MEMBER,
    )

    ActivityEvent.objects.create(
        actor=acting_player,
        event_type=ActivityEvent.TYPE_JOINED_GROUP,
        text_snapshot=f"Joined group {group.name}",
        related_group=group,
        is_public=not group.is_private,
    )

    return membership


@transaction.atomic
def leave_group(*, group, acting_player):
    membership = GroupMembership.objects.filter(group=group, player=acting_player).first()
    if not membership:
        raise ValidationError("You are not a member of this group.")

    if membership.role == GroupMembership.ROLE_OWNER:
        raise PermissionDenied("Group owner cannot leave the group.")

    membership.delete()



def group_feed_queryset(*, group, acting_player):
    if group.is_private and not _is_group_member(group=group, player=acting_player):
        raise PermissionDenied("You must be a group member to view this private group feed.")

    friend_ids = friend_ids_for_player(player=acting_player)

    return (
        SocialPost.objects.select_related("author__user", "group")
        .prefetch_related("comments__author__user", "reactions__player__user")
        .filter(group=group)
        .filter(
            Q(visibility=SocialPost.VISIBILITY_PUBLIC)
            | Q(author=acting_player)
            | Q(visibility=SocialPost.VISIBILITY_FRIENDS_ONLY, author_id__in=friend_ids)
        )
        .order_by("-created_at")
    )
