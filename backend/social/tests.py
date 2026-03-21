from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import ActivityEvent, FriendRequest, Friendship, GroupMembership, SocialGroup, SocialPost


class FriendRequestApiTests(TestCase):
    def setUp(self):
        self.user_a = get_user_model().objects.create_user(username="alice", password="testpass123")
        self.user_b = get_user_model().objects.create_user(username="bob", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_a)

    def test_send_friend_request_creates_pending_request(self):
        response = self.client.post(
            reverse("social-friend-request-list-create"),
            {"to_player_id": self.user_b.player.id},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(FriendRequest.objects.first().status, FriendRequest.STATUS_PENDING)

    def test_reverse_pending_friend_request_returns_validation_error(self):
        FriendRequest.objects.create(from_player=self.user_a.player, to_player=self.user_b.player)

        self.client.force_authenticate(user=self.user_b)
        response = self.client.post(
            reverse("social-friend-request-list-create"),
            {"to_player_id": self.user_a.player.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("already sent you", response.data["detail"])
        self.assertEqual(FriendRequest.objects.filter(status=FriendRequest.STATUS_PENDING).count(), 1)

    def test_accept_friend_request_creates_friendship(self):
        friend_request = FriendRequest.objects.create(from_player=self.user_a.player, to_player=self.user_b.player)

        self.client.force_authenticate(user=self.user_b)
        response = self.client.post(reverse("social-friend-request-accept", args=[friend_request.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friendship.objects.count(), 1)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, FriendRequest.STATUS_ACCEPTED)


class SocialPostApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="poster", password="testpass123")
        self.other_user = get_user_model().objects.create_user(username="other", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_and_update_post(self):
        create_response = self.client.post(
            reverse("social-post-list-create"),
            {
                "content": "First social post",
                "post_type": SocialPost.TYPE_UPDATE,
                "visibility": SocialPost.VISIBILITY_PUBLIC,
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        post_id = create_response.data["id"]

        update_response = self.client.patch(
            reverse("social-post-detail", args=[post_id]),
            {
                "content": "Edited social post",
                "visibility": SocialPost.VISIBILITY_FRIENDS_ONLY,
            },
            format="json",
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["visibility"], SocialPost.VISIBILITY_FRIENDS_ONLY)

    def test_reaction_upsert_and_delete(self):
        post = SocialPost.objects.create(author=self.user.player, content="Hello")

        create_reaction = self.client.put(
            reverse("social-post-reaction", args=[post.id]),
            {"reaction_type": "like"},
            format="json",
        )
        self.assertEqual(create_reaction.status_code, 201)

        update_reaction = self.client.put(
            reverse("social-post-reaction", args=[post.id]),
            {"reaction_type": "fire"},
            format="json",
        )
        self.assertEqual(update_reaction.status_code, 200)

        delete_response = self.client.delete(reverse("social-post-reaction", args=[post.id]))
        self.assertEqual(delete_response.status_code, 204)

    def test_comment_edit_and_delete_ownership_rules(self):
        post = SocialPost.objects.create(author=self.user.player, content="Hello")
        comment_response = self.client.post(
            reverse("social-post-comment-list-create", args=[post.id]),
            {"content": "Original comment"},
            format="json",
        )
        comment_id = comment_response.data["id"]

        self.client.force_authenticate(user=self.other_user)
        unauthorized_edit = self.client.patch(
            reverse("social-post-comment-detail", args=[post.id, comment_id]),
            {"content": "Not allowed"},
            format="json",
        )
        self.assertEqual(unauthorized_edit.status_code, 403)

        unauthorized_delete = self.client.delete(
            reverse("social-post-comment-detail", args=[post.id, comment_id]),
        )
        self.assertEqual(unauthorized_delete.status_code, 403)

        self.client.force_authenticate(user=self.user)
        authorized_edit = self.client.patch(
            reverse("social-post-comment-detail", args=[post.id, comment_id]),
            {"content": "Updated comment"},
            format="json",
        )
        self.assertEqual(authorized_edit.status_code, 200)

        authorized_delete = self.client.delete(reverse("social-post-comment-detail", args=[post.id, comment_id]))
        self.assertEqual(authorized_delete.status_code, 204)


class GroupApiTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="owner", password="testpass123")
        self.member = get_user_model().objects.create_user(username="member", password="testpass123")
        self.viewer = get_user_model().objects.create_user(username="viewer", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.owner)

    def test_create_group_adds_owner_membership(self):
        response = self.client.post(
            reverse("social-group-list-create"),
            {"name": "Focus Guild", "description": "Daily accountability", "is_private": False},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        group_id = response.data["id"]
        self.assertTrue(GroupMembership.objects.filter(group_id=group_id, player=self.owner.player, role="owner").exists())

    def test_join_and_leave_group(self):
        create_response = self.client.post(
            reverse("social-group-list-create"),
            {"name": "Warriors"},
            format="json",
        )
        group_id = create_response.data["id"]

        self.client.force_authenticate(user=self.member)
        join_response = self.client.post(reverse("social-group-join", args=[group_id]))
        self.assertEqual(join_response.status_code, 201)

        leave_response = self.client.post(reverse("social-group-leave", args=[group_id]))
        self.assertEqual(leave_response.status_code, 204)

    def test_group_visibility_public_vs_private(self):
        public_group = SocialGroup.objects.create(name="Public Group", owner=self.owner.player, is_private=False)
        private_group = SocialGroup.objects.create(name="Private Group", owner=self.owner.player, is_private=True)
        GroupMembership.objects.create(group=public_group, player=self.owner.player, role=GroupMembership.ROLE_OWNER)
        GroupMembership.objects.create(group=private_group, player=self.owner.player, role=GroupMembership.ROLE_OWNER)

        self.client.force_authenticate(user=self.viewer)
        list_response = self.client.get(reverse("social-group-list-create"))
        names = {group["name"] for group in list_response.data}

        self.assertIn("Public Group", names)
        self.assertNotIn("Private Group", names)

        feed_forbidden = self.client.get(reverse("social-group-feed", args=[private_group.id]))
        self.assertEqual(feed_forbidden.status_code, 403)


class PublicProfileApiTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="profile_owner", password="testpass123")
        self.viewer = get_user_model().objects.create_user(username="profile_viewer", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.viewer)

    def test_public_profile_includes_recent_activity_and_posts(self):
        post = SocialPost.objects.create(
            author=self.owner.player,
            content="Profile post",
            visibility=SocialPost.VISIBILITY_PUBLIC,
        )
        ActivityEvent.objects.create(
            actor=self.owner.player,
            event_type=ActivityEvent.TYPE_POST_CREATED,
            text_snapshot="Posted an update",
            related_post=post,
        )

        response = self.client.get(reverse("social-public-profile", args=[self.owner.player.id]))

        self.assertEqual(response.status_code, 200)
        self.assertIn("recent_activity", response.data)
        self.assertIn("recent_posts", response.data)
        self.assertEqual(len(response.data["recent_activity"]), 1)
        self.assertEqual(len(response.data["recent_posts"]), 1)
