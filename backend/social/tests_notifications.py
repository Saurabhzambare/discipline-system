"""C3C — ActivityEvent expansion + per-user seen tracking + bounded hooks."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from paths.models import UserPathSelection
from players.models import Player
from quests.models import (
    DailyQuestLineup,
    DailyQuestLineupItem,
    Quest,
)
from quests.services import complete_lineup_item
from social.achievements import award_badge, complete_weekly_boss
from social.models import (
    ActivityEvent,
    ActivityEventRead,
    Badge,
    WeeklyBossQuest,
)

User = get_user_model()


def _make_player(username, *, path="fitness_warrior", level=1, exp=0):
    user = User.objects.create_user(username, password="pw")
    player = Player.objects.get(user=user)
    player.path = path
    player.level = level
    player.exp = exp
    player.save(update_fields=["path", "level", "exp", "updated_at"])
    UserPathSelection.objects.create(
        player=player,
        path=path,
        onboarding_complete=True,
        multi_paths_active=[path],
    )
    return user, player


def _make_event(actor, *, event_type=ActivityEvent.TYPE_QUEST_COMPLETED, snapshot="hi", related_player=None, is_public=True):
    return ActivityEvent.objects.create(
        actor=actor,
        event_type=event_type,
        text_snapshot=snapshot,
        related_player=related_player,
        is_public=is_public,
    )


# ── ActivityEventRead model + uniqueness ─────────────────────────────────────


class ActivityEventReadModelTests(TestCase):
    def test_default_event_is_unseen(self):
        _, player = _make_player("alice")
        event = _make_event(player)
        self.assertFalse(
            ActivityEventRead.objects.filter(event=event, player=player).exists()
        )

    def test_unique_constraint_prevents_duplicate_reads(self):
        _, player = _make_player("alice")
        event = _make_event(player)
        ActivityEventRead.objects.create(event=event, player=player)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ActivityEventRead.objects.create(event=event, player=player)


# ── Notifications endpoint ───────────────────────────────────────────────────


class NotificationsEndpointTests(TestCase):
    def setUp(self):
        self.user, self.player = _make_player("alice")
        self.other_user, self.other_player = _make_player("bob", path="mindset_sage")
        self.client = APIClient()

    def test_endpoint_requires_auth(self):
        url = reverse("social-notifications")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_returns_items_and_unseen_count(self):
        _make_event(self.player, snapshot="A")
        _make_event(self.player, snapshot="B")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("social-notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.data)
        self.assertIn("unseen_count", response.data)
        self.assertEqual(response.data["unseen_count"], 2)
        self.assertEqual(len(response.data["items"]), 2)
        for item in response.data["items"]:
            self.assertFalse(item["is_seen"])
            self.assertIsNone(item["seen_at"])

    def test_unseen_count_excludes_seen_events(self):
        e1 = _make_event(self.player, snapshot="A")
        _make_event(self.player, snapshot="B")
        ActivityEventRead.objects.create(event=e1, player=self.player)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("social-notifications"))
        self.assertEqual(response.data["unseen_count"], 1)

    def test_unseen_events_sort_before_seen_events(self):
        seen = _make_event(self.player, snapshot="seen-old")
        unseen_old = _make_event(self.player, snapshot="unseen-old")
        unseen_new = _make_event(self.player, snapshot="unseen-new")
        ActivityEventRead.objects.create(event=seen, player=self.player)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("social-notifications"))
        ids = [item["id"] for item in response.data["items"]]
        # Unseen first (newest first within group), then seen
        self.assertEqual(ids[0], unseen_new.id)
        self.assertEqual(ids[1], unseen_old.id)
        self.assertEqual(ids[2], seen.id)

    def test_does_not_expose_unrelated_player_events(self):
        _make_event(self.other_player, snapshot="bob's quest")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("social-notifications"))
        self.assertEqual(response.data["unseen_count"], 0)
        self.assertEqual(len(response.data["items"]), 0)

    def test_includes_events_where_player_is_related(self):
        # Bob added Alice as friend → event on bob with related_player=alice
        _make_event(
            self.other_player,
            event_type=ActivityEvent.TYPE_FRIEND_ADDED,
            snapshot="bob friended alice",
            related_player=self.player,
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("social-notifications"))
        self.assertEqual(response.data["unseen_count"], 1)


# ── mark-seen endpoint ───────────────────────────────────────────────────────


class NotificationsMarkSeenTests(TestCase):
    def setUp(self):
        self.user, self.player = _make_player("alice")
        self.other_user, self.other_player = _make_player("bob", path="mindset_sage")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_marks_visible_events_as_seen(self):
        e1 = _make_event(self.player)
        e2 = _make_event(self.player)
        response = self.client.post(
            reverse("social-notifications-mark-seen"),
            {"event_ids": [e1.id, e2.id]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["marked"], 2)
        self.assertEqual(response.data["unseen_count"], 0)
        self.assertTrue(
            ActivityEventRead.objects.filter(event=e1, player=self.player).exists()
        )

    def test_empty_list_returns_zero_marked_and_current_unseen(self):
        _make_event(self.player)
        response = self.client.post(
            reverse("social-notifications-mark-seen"),
            {"event_ids": []},
            format="json",
        )
        self.assertEqual(response.data["marked"], 0)
        self.assertEqual(response.data["unseen_count"], 1)

    def test_already_seen_event_not_remarked(self):
        e1 = _make_event(self.player)
        original = ActivityEventRead.objects.create(event=e1, player=self.player)
        original_seen_at = original.seen_at
        response = self.client.post(
            reverse("social-notifications-mark-seen"),
            {"event_ids": [e1.id]},
            format="json",
        )
        self.assertEqual(response.data["marked"], 0)
        original.refresh_from_db()
        self.assertEqual(original.seen_at, original_seen_at)

    def test_invisible_other_user_event_not_marked(self):
        invisible = _make_event(self.other_player)
        response = self.client.post(
            reverse("social-notifications-mark-seen"),
            {"event_ids": [invisible.id]},
            format="json",
        )
        self.assertEqual(response.data["marked"], 0)
        self.assertFalse(
            ActivityEventRead.objects.filter(event=invisible, player=self.player).exists()
        )

    def test_returns_updated_unseen_count(self):
        e1 = _make_event(self.player)
        _make_event(self.player)  # remains unseen
        response = self.client.post(
            reverse("social-notifications-mark-seen"),
            {"event_ids": [e1.id]},
            format="json",
        )
        self.assertEqual(response.data["marked"], 1)
        self.assertEqual(response.data["unseen_count"], 1)


# ── Event hook tests ─────────────────────────────────────────────────────────


class EventHookTests(TestCase):
    def setUp(self):
        call_command("seed_badges")

    def _build_lineup_item(self, player, *, exp_reward=40):
        quest = Quest.objects.create(
            title="Test Quest",
            exp_reward=exp_reward,
            rank="D",
            path_target=player.path,
            pillar="body",
        )
        today = timezone.localdate()
        lineup = DailyQuestLineup.objects.create(player=player, path=player.path, date=today)
        item = DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=quest,
            slot_order=1,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
        )
        return item

    def test_complete_lineup_item_creates_quest_completed_event(self):
        _, player = _make_player("alice")
        item = self._build_lineup_item(player)
        complete_lineup_item(player, item.id)
        events = ActivityEvent.objects.filter(actor=player, event_type=ActivityEvent.TYPE_QUEST_COMPLETED)
        self.assertEqual(events.count(), 1)
        self.assertIn("alice", events.first().text_snapshot)
        self.assertIn("Test Quest", events.first().text_snapshot)

    def test_level_up_creates_level_up_event(self):
        # Level 1 → level 2 boundary is 150 EXP. Award a quest worth 200 EXP.
        _, player = _make_player("levelupper", exp=140)
        item = self._build_lineup_item(player, exp_reward=200)
        complete_lineup_item(player, item.id)
        level_events = ActivityEvent.objects.filter(
            actor=player, event_type=ActivityEvent.TYPE_LEVEL_UP
        )
        self.assertEqual(level_events.count(), 1)
        self.assertIn("Level", level_events.first().text_snapshot)

    def test_no_level_up_event_when_level_unchanged(self):
        _, player = _make_player("steady", exp=10)
        item = self._build_lineup_item(player, exp_reward=10)
        complete_lineup_item(player, item.id)
        self.assertFalse(
            ActivityEvent.objects.filter(actor=player, event_type=ActivityEvent.TYPE_LEVEL_UP).exists()
        )

    def test_award_badge_creates_badge_earned_event_only_on_new(self):
        _, player = _make_player("badgee")
        # First call creates event.
        award_badge(player, "streak_7")
        first_count = ActivityEvent.objects.filter(
            actor=player, event_type=ActivityEvent.TYPE_BADGE_EARNED
        ).count()
        self.assertEqual(first_count, 1)
        # Second idempotent call does not create another.
        award_badge(player, "streak_7")
        second_count = ActivityEvent.objects.filter(
            actor=player, event_type=ActivityEvent.TYPE_BADGE_EARNED
        ).count()
        self.assertEqual(second_count, 1)

    def test_complete_weekly_boss_creates_weekly_boss_defeated_event(self):
        _, player = _make_player("hunter")
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        boss = WeeklyBossQuest.objects.create(
            path_target=player.path,
            week_start=week_start,
            title="Iron Test",
            exp_reward=500,
            is_active=True,
        )
        result = complete_weekly_boss(player, boss.id)
        self.assertFalse(result.get("already_completed"))
        events = ActivityEvent.objects.filter(
            actor=player, event_type=ActivityEvent.TYPE_WEEKLY_BOSS_DEFEATED
        )
        self.assertEqual(events.count(), 1)
        self.assertIn("Iron Test", events.first().text_snapshot)

        # Duplicate call should not duplicate event.
        complete_weekly_boss(player, boss.id)
        self.assertEqual(
            ActivityEvent.objects.filter(
                actor=player, event_type=ActivityEvent.TYPE_WEEKLY_BOSS_DEFEATED
            ).count(),
            1,
        )

    def test_cross_path_title_activation_creates_event(self):
        from paths.services import complete_path_onboarding

        _, player = _make_player("cross", path="fitness_warrior")
        # Activate two paths so warrior_sage qualifies.
        UserPathSelection.objects.filter(player=player).update(
            multi_paths_active=["fitness_warrior", "mindset_sage"]
        )
        complete_path_onboarding(player, "mindset_sage")
        events = ActivityEvent.objects.filter(
            actor=player, event_type=ActivityEvent.TYPE_CROSS_PATH_TITLE_EARNED
        )
        self.assertGreaterEqual(events.count(), 1)
        self.assertIn("title", events.first().text_snapshot.lower())
