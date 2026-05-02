"""HTTP API endpoints for social features with thin view logic."""

from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Exists, OuterRef
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from players.models import Player

from .models import (
    ActivityEvent,
    ActivityEventRead,
    FriendRequest,
    GroupMembership,
    PostComment,
    PostReaction,
    SocialGroup,
)
from .selectors import (
    profile_achievement_cards_selector,
    profile_activity_queryset,
    profile_badges_selector,
    profile_path_profiles_selector,
    profile_posts_queryset,
    visible_groups_queryset_for_player,
    visible_post_queryset_for_player,
    visible_posts_queryset_for_player,
)
from .serializers import (
    AccountabilityRequestCreateSerializer,
    AccountabilityRequestSerializer,
    FriendRequestCreateSerializer,
    FriendRequestSerializer,
    FriendshipListSerializer,
    GroupCreateSerializer,
    GroupMembershipSerializer,
    GroupSerializer,
    PostCommentCreateSerializer,
    PostCommentSerializer,
    PostCommentUpdateSerializer,
    PostReactionSerializer,
    PostReactionUpsertSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PublicProfileSerializer,
    SocialPostSerializer,
)
from .services.leaderboards import (
    armor_leaderboard,
    global_cross_path_leaderboard,
    multiplier_streak_leaderboard,
    output_log_monthly_leaderboard,
    weekly_exp_leaderboard,
)
from .services import (
    SocialNotFoundError,
    accept_accountability_request,
    accept_friend_request,
    add_comment,
    add_or_update_reaction,
    cancel_friend_request,
    create_group,
    create_post,
    decline_friend_request,
    delete_comment,
    delete_post,
    friend_requests_queryset,
    get_group_or_404,
    get_public_profile_player,
    group_feed_queryset,
    join_group,
    leave_group,
    list_accountability_requests_queryset,
    list_friends_queryset,
    reject_accountability_request,
    remove_friend,
    remove_reaction,
    send_accountability_request,
    send_friend_request,
    update_comment,
    update_post,
)


def _error_response(*, detail, status_code):
    return Response({"detail": detail}, status=status_code)


class SocialBaseView(APIView):
    """Base view with shared error handling helpers."""

    permission_classes = [IsAuthenticated]

    @staticmethod
    def bad_request(error):
        return _error_response(detail=error.message, status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def forbidden(error):
        return _error_response(detail=error.args[0], status_code=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def not_found(error):
        return _error_response(detail=str(error), status_code=status.HTTP_404_NOT_FOUND)


class FriendRequestListCreateView(SocialBaseView):
    def get(self, request):
        direction = request.query_params.get("direction")
        requests_qs = friend_requests_queryset(player=request.user.player, direction=direction)
        serializer = FriendRequestSerializer(requests_qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FriendRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            friend_request = send_friend_request(
                from_player=request.user.player,
                to_player_id=serializer.validated_data["to_player_id"],
            )
        except ValidationError as error:
            return self.bad_request(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)


class AccountabilityRequestListCreateView(SocialBaseView):
    def get(self, request):
        direction = request.query_params.get("direction")
        requests_qs = list_accountability_requests_queryset(player=request.user.player, direction=direction)
        serializer = AccountabilityRequestSerializer(requests_qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountabilityRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            partner_request = send_accountability_request(
                from_player=request.user.player,
                to_player_id=serializer.validated_data["to_player_id"],
            )
        except ValidationError as error:
            return self.bad_request(error)
        except SocialNotFoundError as error:
            return self.not_found(error)
        return Response(AccountabilityRequestSerializer(partner_request).data, status=status.HTTP_201_CREATED)


class AccountabilityRequestAcceptView(SocialBaseView):
    def post(self, request, request_id):
        try:
            partnership = accept_accountability_request(request_id=request_id, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        partner_player = partnership.player_two if partnership.player_one_id == request.user.player.id else partnership.player_one
        return Response({"id": partner_player.id, "username": partner_player.user.username})


class AccountabilityRequestRejectView(SocialBaseView):
    def post(self, request, request_id):
        try:
            partner_request = reject_accountability_request(request_id=request_id, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(AccountabilityRequestSerializer(partner_request).data)


class FriendRequestAcceptView(SocialBaseView):
    def post(self, request, request_id):
        try:
            friendship = accept_friend_request(request_id=request_id, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        friend_player = friendship.player_two if friendship.player_one_id == request.user.player.id else friendship.player_one
        payload = {"id": friend_player.id, "username": friend_player.user.username}
        return Response(payload)


class FriendRequestDeclineView(SocialBaseView):
    def post(self, request, request_id):
        try:
            friend_request = decline_friend_request(request_id=request_id, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(FriendRequestSerializer(friend_request).data)


class FriendRequestCancelView(SocialBaseView):
    def post(self, request, request_id):
        try:
            friend_request = cancel_friend_request(request_id=request_id, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(FriendRequestSerializer(friend_request).data)


class FriendsListView(SocialBaseView):
    def get(self, request):
        friendships = list_friends_queryset(player=request.user.player)
        friend_payloads = []
        for friendship in friendships:
            friend_player = friendship.player_two if friendship.player_one_id == request.user.player.id else friendship.player_one
            friend_payloads.append({"id": friend_player.id, "username": friend_player.user.username})

        serializer = FriendshipListSerializer(friend_payloads, many=True)
        return Response(serializer.data)


class FriendRemoveView(SocialBaseView):
    def delete(self, request, player_id):
        try:
            remove_friend(acting_player=request.user.player, other_player_id=player_id)
        except ValidationError as error:
            return self.bad_request(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicProfileView(SocialBaseView):
    """Public player profile with progression summary, activity, and recent posts."""

    def get(self, request, identifier):
        try:
            player = get_public_profile_player(identifier=identifier)
        except SocialNotFoundError as error:
            return self.not_found(error)

        request_player = getattr(request.user, "player", None)
        is_own_profile = bool(request_player and request_player.id == player.id)

        payload = {
            "id": player.id,
            "username": player.user.username,
            "level": player.level,
            "exp": player.exp,
            "streak": player.streak,
            "recent_activity": profile_activity_queryset(target_player=player)[:20],
            "recent_posts": profile_posts_queryset(target_player=player)[:10],
            "is_own_profile": is_own_profile,
            "path_profiles": profile_path_profiles_selector(player=player, is_own_profile=is_own_profile),
            "badges": profile_badges_selector(player=player),
            "achievement_cards": profile_achievement_cards_selector(player=player),
        }

        serializer = PublicProfileSerializer(payload)
        return Response(serializer.data)


class SocialPostListCreateView(SocialBaseView):
    def get(self, request):
        posts = visible_posts_queryset_for_player(player=request.user.player)
        return Response(SocialPostSerializer(posts, many=True).data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = create_post(
                author=request.user.player,
                content=serializer.validated_data["content"],
                post_type=serializer.validated_data["post_type"],
                visibility=serializer.validated_data["visibility"],
                group_id=serializer.validated_data.get("group_id"),
            )
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(SocialPostSerializer(post).data, status=status.HTTP_201_CREATED)


class SocialPostDetailView(SocialBaseView):
    def get_object(self, request, post_id):
        post = visible_post_queryset_for_player(player=request.user.player, post_id=post_id).first()
        if not post:
            raise SocialNotFoundError("Post not found.")
        return post

    def get(self, request, post_id):
        try:
            post = self.get_object(request, post_id)
        except SocialNotFoundError as error:
            return self.not_found(error)
        return Response(SocialPostSerializer(post).data)

    def patch(self, request, post_id):
        serializer = PostUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = self.get_object(request, post_id)
            updated = update_post(
                post=post,
                acting_player=request.user.player,
                content=serializer.validated_data["content"],
                visibility=serializer.validated_data["visibility"],
            )
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(SocialPostSerializer(updated).data)

    def delete(self, request, post_id):
        try:
            post = self.get_object(request, post_id)
            delete_post(post=post, acting_player=request.user.player)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentListCreateView(SocialBaseView):
    def get(self, request, post_id):
        post = visible_post_queryset_for_player(player=request.user.player, post_id=post_id).first()
        if not post:
            return self.not_found(SocialNotFoundError("Post not found."))

        comment_qs = post.comments.select_related("author__user").all().order_by("created_at")
        return Response(PostCommentSerializer(comment_qs, many=True).data)

    def post(self, request, post_id):
        serializer = PostCommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = visible_post_queryset_for_player(player=request.user.player, post_id=post_id).first()
        if not post:
            return self.not_found(SocialNotFoundError("Post not found."))

        comment = add_comment(post=post, acting_player=request.user.player, content=serializer.validated_data["content"])
        return Response(PostCommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class PostCommentDetailView(SocialBaseView):
    """Edit/delete endpoint for comments with author ownership checks."""

    def get_object(self, request, post_id, comment_id):
        comment = (
            PostComment.objects.select_related("author__user", "post")
            .filter(id=comment_id, post_id=post_id)
            .first()
        )
        if not comment:
            raise SocialNotFoundError("Comment not found.")

        post_visible = visible_post_queryset_for_player(player=request.user.player, post_id=post_id).exists()
        if not post_visible:
            raise SocialNotFoundError("Post not found.")

        return comment

    def patch(self, request, post_id, comment_id):
        serializer = PostCommentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            comment = self.get_object(request, post_id, comment_id)
            updated = update_comment(
                comment=comment,
                acting_player=request.user.player,
                content=serializer.validated_data["content"],
            )
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(PostCommentSerializer(updated).data)

    def delete(self, request, post_id, comment_id):
        try:
            comment = self.get_object(request, post_id, comment_id)
            delete_comment(comment=comment, acting_player=request.user.player)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostReactionView(SocialBaseView):
    def put(self, request, post_id):
        serializer = PostReactionUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = visible_post_queryset_for_player(player=request.user.player, post_id=post_id).first()
        if not post:
            return self.not_found(SocialNotFoundError("Post not found."))

        reaction, created = add_or_update_reaction(
            post=post,
            acting_player=request.user.player,
            reaction_type=serializer.validated_data["reaction_type"],
        )
        code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(PostReactionSerializer(reaction).data, status=code)

    def delete(self, request, post_id):
        post = visible_post_queryset_for_player(player=request.user.player, post_id=post_id).first()
        if not post:
            return self.not_found(SocialNotFoundError("Post not found."))

        try:
            remove_reaction(post=post, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupListCreateView(SocialBaseView):
    def get(self, request):
        groups = visible_groups_queryset_for_player(player=request.user.player).annotate(
            member_count=Count("memberships"),
            is_member=Exists(
                GroupMembership.objects.filter(group=OuterRef("pk"), player=request.user.player)
            ),
        )
        return Response(GroupSerializer(groups, many=True).data)

    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = create_group(
            owner=request.user.player,
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description", ""),
            is_private=serializer.validated_data.get("is_private", False),
        )
        group = SocialGroup.objects.select_related("owner__user").annotate(member_count=Count("memberships")).get(id=group.id)
        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class GroupJoinView(SocialBaseView):
    def post(self, request, group_id):
        try:
            group = get_group_or_404(group_id=group_id)
            membership = join_group(group=group, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(GroupMembershipSerializer(membership).data, status=status.HTTP_201_CREATED)


class GroupLeaveView(SocialBaseView):
    def post(self, request, group_id):
        try:
            group = get_group_or_404(group_id=group_id)
            leave_group(group=group, acting_player=request.user.player)
        except ValidationError as error:
            return self.bad_request(error)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMembershipListView(SocialBaseView):
    def get(self, request, group_id):
        try:
            group = get_group_or_404(group_id=group_id)
        except SocialNotFoundError as error:
            return self.not_found(error)

        if group.is_private and not group.memberships.filter(player=request.user.player).exists():
            return self.forbidden(PermissionDenied("You must be a group member to view private group members."))

        memberships = group.memberships.select_related("player__user").all().order_by("joined_at")
        return Response(GroupMembershipSerializer(memberships, many=True).data)


class GroupFeedView(SocialBaseView):
    def get(self, request, group_id):
        try:
            group = get_group_or_404(group_id=group_id)
            posts = group_feed_queryset(group=group, acting_player=request.user.player)
        except PermissionDenied as error:
            return self.forbidden(error)
        except SocialNotFoundError as error:
            return self.not_found(error)

        return Response(SocialPostSerializer(posts, many=True).data)


class PlayerSearchView(SocialBaseView):
    """Search players by username prefix for friend discovery."""

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if len(q) < 2:
            return Response([])

        players = (
            Player.objects.select_related("user")
            .filter(user__username__icontains=q)
            .exclude(id=request.user.player.id)
            .order_by("user__username")[:10]
        )

        results = [
            {"id": p.id, "username": p.user.username, "level": p.level}
            for p in players
        ]
        return Response(results)


def _visible_notifications_qs(player):
    """ActivityEvents visible to ``player`` for notification purposes.

    Includes events where the player is the actor (their own progression
    history) and events where the player is the related_player (e.g. someone
    added them as a friend).
    """
    from django.db.models import Q

    return (
        ActivityEvent.objects.select_related("actor__user", "related_player__user")
        .filter(Q(actor=player) | Q(related_player=player))
    )


class NotificationsView(SocialBaseView):
    """Per-player notification feed backed by ActivityEvent + ActivityEventRead."""

    DEFAULT_LIMIT = 25

    def get(self, request):
        player = request.user.player
        events_qs = _visible_notifications_qs(player)

        seen_event_ids = set(
            ActivityEventRead.objects.filter(player=player, event__in=events_qs)
            .values_list("event_id", flat=True)
        )
        seen_at_by_event = dict(
            ActivityEventRead.objects.filter(player=player, event__in=events_qs)
            .values_list("event_id", "seen_at")
        )

        ordered = list(events_qs.order_by("-created_at", "-id")[: self.DEFAULT_LIMIT * 2])

        items = []
        for event in ordered:
            seen_at = seen_at_by_event.get(event.id)
            items.append({
                "id": event.id,
                "event_type": event.event_type,
                "text_snapshot": event.text_snapshot,
                "actor": {"id": event.actor_id, "username": event.actor.user.username},
                "related_player_id": event.related_player_id,
                "related_post_id": event.related_post_id,
                "related_group_id": event.related_group_id,
                "created_at": event.created_at.isoformat(),
                "seen_at": seen_at.isoformat() if seen_at else None,
                "is_seen": event.id in seen_event_ids,
            })

        # Stable sort: unseen group first, then created_at desc, then id desc.
        items.sort(key=lambda x: x["id"], reverse=True)
        items.sort(key=lambda x: x["created_at"], reverse=True)
        items.sort(key=lambda x: 0 if not x["is_seen"] else 1)

        items = items[: self.DEFAULT_LIMIT]

        unseen_count = events_qs.exclude(id__in=seen_event_ids).count()
        return Response({"items": items, "unseen_count": unseen_count})


class NotificationsMarkSeenView(SocialBaseView):
    """POST endpoint to mark a list of visible events as seen for the player."""

    def post(self, request):
        player = request.user.player
        raw_ids = request.data.get("event_ids", [])
        if not isinstance(raw_ids, list):
            return _error_response(detail="event_ids must be a list.", status_code=status.HTTP_400_BAD_REQUEST)

        event_ids = []
        for v in raw_ids:
            try:
                event_ids.append(int(v))
            except (TypeError, ValueError):
                return _error_response(detail="event_ids must be integers.", status_code=status.HTTP_400_BAD_REQUEST)

        events_qs = _visible_notifications_qs(player)

        marked = 0
        if event_ids:
            visible_ids = set(
                events_qs.filter(id__in=event_ids).values_list("id", flat=True)
            )
            already_seen_ids = set(
                ActivityEventRead.objects.filter(player=player, event_id__in=visible_ids)
                .values_list("event_id", flat=True)
            )
            to_create = visible_ids - already_seen_ids
            for event_id in to_create:
                _, created = ActivityEventRead.objects.get_or_create(
                    player=player, event_id=event_id
                )
                if created:
                    marked += 1

        seen_event_ids = set(
            ActivityEventRead.objects.filter(player=player, event__in=events_qs)
            .values_list("event_id", flat=True)
        )
        unseen_count = events_qs.exclude(id__in=seen_event_ids).count()

        return Response({"marked": marked, "unseen_count": unseen_count})


# ── LEADERBOARDS ─────────────────────────────────────────────────────────────

PATH_VALUES = {value for value, _label in Player.PATH_CHOICES}


class _LeaderboardBaseView(SocialBaseView):
    def _limit(self, request):
        raw = request.query_params.get("limit")
        if raw is None:
            return 10
        try:
            return int(raw)
        except ValueError:
            return 10


class WeeklyLeaderboardView(_LeaderboardBaseView):
    def get(self, request, path):
        if path not in PATH_VALUES:
            return _error_response(detail="Unknown path.", status_code=status.HTTP_404_NOT_FOUND)
        data = weekly_exp_leaderboard(
            path=path,
            limit=self._limit(request),
            requesting_player=request.user.player,
        )
        return Response(data)


class GlobalLeaderboardView(_LeaderboardBaseView):
    def get(self, request):
        data = global_cross_path_leaderboard(
            limit=self._limit(request),
            requesting_player=request.user.player,
        )
        return Response(data)


class ArmorLeaderboardView(_LeaderboardBaseView):
    def get(self, request):
        data = armor_leaderboard(
            limit=self._limit(request),
            requesting_player=request.user.player,
        )
        return Response(data)


class MultiplierStreakLeaderboardView(_LeaderboardBaseView):
    def get(self, request):
        data = multiplier_streak_leaderboard(
            limit=self._limit(request),
            requesting_player=request.user.player,
        )
        return Response(data)


class OutputMonthlyLeaderboardView(_LeaderboardBaseView):
    def get(self, request):
        data = output_log_monthly_leaderboard(
            limit=self._limit(request),
            requesting_player=request.user.player,
        )
        return Response(data)
