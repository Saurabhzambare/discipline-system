"""HTTP API endpoints for social features with thin view logic."""

from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PostComment, SocialGroup
from .selectors import (
    profile_activity_queryset,
    profile_posts_queryset,
    visible_groups_queryset_for_player,
    visible_post_queryset_for_player,
    visible_posts_queryset_for_player,
)
from .serializers import (
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
from .services import (
    SocialNotFoundError,
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
    list_friends_queryset,
    remove_friend,
    remove_reaction,
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

        payload = {
            "id": player.id,
            "username": player.user.username,
            "level": player.level,
            "exp": player.exp,
            "streak": player.streak,
            "recent_activity": profile_activity_queryset(target_player=player)[:20],
            "recent_posts": profile_posts_queryset(target_player=player)[:10],
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
        groups = visible_groups_queryset_for_player(player=request.user.player).annotate(member_count=Count("memberships"))
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
