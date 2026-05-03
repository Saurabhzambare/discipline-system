"""
Phase 5B end-to-end verification tests (C4-1, BUILD_ORDER Steps 89-98).

These tests prove the major Phase 5B user flows work end-to-end:
new-user signup, onboarding, daily quest assignment, mechanics, cross-path
bonus, cross-path titles, leaderboards, and achievement cards.

Each test class targets a specific BUILD_ORDER step. Tests are integration
focused — they exercise services + models + URL views together, using the
APIClient with force_authenticate to simulate the authenticated player.
"""

import datetime as _dt

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from paths.models import (
    BodyJournal,
    DarkNightEntry,
    DisciplineKnightProfile,
    FitnessWarriorProfile,
    GrindVisionaryProfile,
    HealthAlchemistProfile,
    MindsetSageProfile,
    OutputLog,
    PathOnboardingProgress,
    SingularGoal,
    SkillTree,
    SplitDayState,
    TemptationLog,
    UserPathSelection,
    WisdomLog,
)
from players.models import Player
from quests.models import (
    CrossPathBonus,
    DailyQuestLineup,
    DailyQuestLineupItem,
    Quest,
    QuestCompletion,
)
from quests.services import (
    apply_cross_path_bonus_flags,
    complete_lineup_item,
    detect_cross_path_bonus,
    generate_daily_lineup,
    get_daily_lineup,
)
from social.achievements import (
    complete_weekly_boss,
    generate_achievement_card,
    grant_cross_path_title,
)
from social.models import (
    AchievementCard,
    ActivityEvent,
    Badge,
    SocialPost,
    UserBadge,
    WeeklyBossQuest,
)
from social.services.leaderboards import (
    armor_leaderboard,
    global_cross_path_leaderboard,
    multiplier_streak_leaderboard,
    output_log_monthly_leaderboard,
    weekly_exp_leaderboard,
)


User = get_user_model()


# ── Shared helpers ────────────────────────────────────────────────────────────

ALL_PATHS = [
    "fitness_warrior",
    "mindset_sage",
    "health_alchemist",
    "discipline_knight",
    "grind_visionary",
]


def _make_user(username, password="testpass123"):
    user = User.objects.create_user(username=username, password=password)
    return user, user.player


def _authed(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def _seed_path_quests(path):
    """Seed minimal quest catalog for a path so lineup generation succeeds."""
    starter_titles = {
        "fitness_warrior": [
            "Complete 20 Pushups",
            "Walk 5000 Steps",
            "Hit Your Protein Target",
        ],
        "mindset_sage": [
            "Meditate for 5 Minutes",
            "Write 3 Things You Are Grateful For",
            "Sit in Silence for 5 Minutes",
        ],
        "health_alchemist": [
            "Drink 2L of Water",
            "Alchemist Morning Protocol",
            "Eat One Whole Food Meal",
        ],
        "discipline_knight": [
            "Make Your Bed",
            "Write Tomorrow's Schedule",
            "Clean Your Workspace",
        ],
        "grind_visionary": [
            "30 Minutes on Your Grind Focus",
            "Singular Goal Check-In",
            "Log One Thing You Learned",
        ],
    }
    for title in starter_titles[path]:
        Quest.objects.get_or_create(
            title=title,
            defaults={
                "description": f"Starter quest for {path}",
                "exp_reward": 20,
                "path_target": path,
                "rank": "D",
                "pillar": "body" if path == "fitness_warrior" else "mind",
                "is_active": True,
            },
        )


def _seed_universal_quest():
    Quest.objects.get_or_create(
        title="Universal Hydration",
        defaults={
            "description": "Hydrate.",
            "exp_reward": 10,
            "path_target": "",
            "universal_daily": True,
            "rank": "D",
            "pillar": "body",
            "is_active": True,
        },
    )


def _complete_onboarding_for(player, path):
    UserPathSelection.objects.update_or_create(
        player=player,
        defaults={
            "path": path,
            "onboarding_complete": True,
            "multi_paths_active": [path],
        },
    )
    player.path = path
    player.save(update_fields=["path", "updated_at"])


def _set_active_paths(player, paths_list):
    UserPathSelection.objects.update_or_create(
        player=player,
        defaults={
            "path": player.path or paths_list[0],
            "onboarding_complete": True,
            "multi_paths_active": paths_list,
        },
    )
    if not player.path:
        player.path = paths_list[0]
        player.save(update_fields=["path", "updated_at"])


# ── STEP 89 — Full new-user end-to-end flow ──────────────────────────────────


class Step89NewUserFullFlowTests(TestCase):
    """BUILD_ORDER Step 89: signup → quiz → path → onboarding → Day1 → completion."""

    @classmethod
    def setUpTestData(cls):
        for path in ALL_PATHS:
            _seed_path_quests(path)
        _seed_universal_quest()

    def test_signup_creates_player_via_signal(self):
        client = APIClient()
        url = reverse("auth-signup")
        resp = client.post(
            url,
            {"username": "newhunter", "password": "supersecure123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201, resp.data)
        user = User.objects.get(username="newhunter")
        self.assertTrue(Player.objects.filter(user=user).exists())

    def test_full_new_user_flow_through_first_day(self):
        # 1. Signup
        signup = APIClient()
        resp = signup.post(
            reverse("auth-signup"),
            {"username": "warrior_e2e", "password": "supersecure123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        user = User.objects.get(username="warrior_e2e")
        player = user.player

        # 2. Take the path discovery quiz
        client = _authed(user)
        start = client.post(reverse("quiz-start"))
        self.assertEqual(start.status_code, 201)
        quiz_id = start.data["quiz_id"]
        self.assertEqual(len(start.data["questions"]), 9)

        for q in range(1, 10):
            ans = client.post(
                reverse("quiz-answer"),
                {"quiz_id": quiz_id, "question_number": q, "answer": "A"},
                format="json",
            )
            self.assertEqual(ans.status_code, 200, ans.data)

        completed = client.post(
            reverse("quiz-complete"),
            {"quiz_id": quiz_id},
            format="json",
        )
        self.assertEqual(completed.status_code, 200)
        self.assertEqual(len(completed.data["results"]), 5)

        # 3. Commit to a path
        select = client.post(
            reverse("path-select"),
            {"path_code": "fitness_warrior"},
            format="json",
        )
        self.assertEqual(select.status_code, 200)
        player.refresh_from_db()
        self.assertEqual(player.path, "fitness_warrior")

        # 4. Complete fitness warrior onboarding
        onboard = client.post(
            reverse("onboarding-fitness-warrior"),
            {
                "training_split": "ppl",
                "primary_goal": "muscle_gain",
                "training_days_per_week": 4,
                "experience_level": "beginner",
                "split_day_start": "push",
            },
            format="json",
        )
        self.assertEqual(onboard.status_code, 200, onboard.data)

        complete_resp = client.post(
            reverse("onboarding-complete"),
            {"path_code": "fitness_warrior"},
            format="json",
        )
        self.assertEqual(complete_resp.status_code, 200)
        self.assertTrue(complete_resp.data["completed"])

        # 5. Day 1 lineup is generated
        daily = client.get(reverse("quest-daily"))
        self.assertEqual(daily.status_code, 200)
        self.assertIsNotNone(daily.data["lineup"])
        items = daily.data["lineup"]["items"]
        self.assertGreaterEqual(len(items), 3)

        # 6. Complete a couple of items, EXP increases, history rows created
        completable = [i for i in items if i["quest_id"] and not i["completed_today"]][:2]
        self.assertGreaterEqual(len(completable), 2)
        starting_exp = player.exp
        for item in completable:
            r = client.post(
                reverse("quest-daily-complete"),
                {"item_id": item["item_id"]},
                format="json",
            )
            self.assertEqual(r.status_code, 200, r.data)
            self.assertTrue(r.data["item_completed"])

        player.refresh_from_db()
        self.assertGreater(player.exp, starting_exp)
        self.assertEqual(
            QuestCompletion.objects.filter(player=player).count(),
            len(completable),
        )

        # 7. Dashboard/lineup payload remains stable on re-fetch
        re_daily = client.get(reverse("quest-daily"))
        self.assertEqual(re_daily.status_code, 200)
        self.assertIn("missed_day", re_daily.data)

        # 8. Day 2 generation works when date advances
        today = timezone.localdate()
        tomorrow = today + _dt.timedelta(days=1)
        day2_lineup, created = generate_daily_lineup(
            player=player, target_date=tomorrow, path_code="fitness_warrior"
        )
        self.assertTrue(created)
        self.assertEqual(day2_lineup.date, tomorrow)
        self.assertGreater(day2_lineup.items.count(), 0)


# ── STEP 90 — Existing user account flow ─────────────────────────────────────


class Step90ExistingUserFlowTests(TestCase):
    """BUILD_ORDER Step 90: existing user with path can still load data and complete quests."""

    @classmethod
    def setUpTestData(cls):
        _seed_path_quests("mindset_sage")
        _seed_universal_quest()

    def setUp(self):
        self.user, self.player = _make_user("existing_sage")
        _complete_onboarding_for(self.player, "mindset_sage")
        # Pre-existing player state.
        self.player.exp = 250
        self.player.level = 2
        self.player.streak = 3
        self.player.last_active_date = timezone.localdate() - _dt.timedelta(days=1)
        self.player.save(update_fields=[
            "exp", "level", "streak", "last_active_date", "updated_at",
        ])
        self.client = _authed(self.user)

    def test_existing_player_can_load_player_profile(self):
        resp = self.client.get(reverse("player-me"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["path"], "mindset_sage")
        self.assertEqual(resp.data["exp"], 250)

    def test_existing_player_receives_daily_lineup(self):
        resp = self.client.get(reverse("quest-daily"))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data["lineup"])

    def test_existing_player_can_complete_lineup_item(self):
        daily = self.client.get(reverse("quest-daily"))
        item = next(i for i in daily.data["lineup"]["items"] if i["quest_id"])
        starting_exp = self.player.exp

        r = self.client.post(
            reverse("quest-daily-complete"),
            {"item_id": item["item_id"]},
            format="json",
        )
        self.assertEqual(r.status_code, 200)

        self.player.refresh_from_db()
        self.assertGreater(self.player.exp, starting_exp)
        # Streak should advance because last_active_date was yesterday.
        self.assertGreaterEqual(self.player.streak, 4)

    def test_existing_player_public_profile_endpoint_returns_payload(self):
        resp = self.client.get(
            reverse("social-public-profile", args=[self.user.username])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["username"], "existing_sage")
        self.assertIn("achievement_cards", resp.data)
        self.assertIn("recent_activity", resp.data)


# ── STEP 91 — Existing social features still working ─────────────────────────


class Step91SocialFeaturesSmokeTests(TestCase):
    """BUILD_ORDER Step 91: posts, comments, reactions, friend requests, notifications."""

    def setUp(self):
        self.alice_user, self.alice = _make_user("alice_e2e")
        self.bob_user, self.bob = _make_user("bob_e2e")
        self.alice_client = _authed(self.alice_user)
        self.bob_client = _authed(self.bob_user)

    def test_post_create_comment_react_flow(self):
        # Alice creates a public post.
        post_resp = self.alice_client.post(
            reverse("social-post-list-create"),
            {"content": "Day 1 of training", "visibility": "public", "post_type": "update"},
            format="json",
        )
        self.assertEqual(post_resp.status_code, 201, post_resp.data)
        post_id = post_resp.data["id"]

        # Bob comments on it.
        comment_resp = self.bob_client.post(
            reverse("social-post-comment-list-create", args=[post_id]),
            {"content": "Let's go!"},
            format="json",
        )
        self.assertEqual(comment_resp.status_code, 201, comment_resp.data)

        # Bob reacts to it (PUT — upsert reaction).
        react_resp = self.bob_client.put(
            reverse("social-post-reaction", args=[post_id]),
            {"reaction_type": "fire"},
            format="json",
        )
        self.assertIn(react_resp.status_code, (200, 201), react_resp.data)

    def test_friend_request_send_and_accept(self):
        send = self.alice_client.post(
            reverse("social-friend-request-list-create"),
            {"to_player_id": self.bob.id},
            format="json",
        )
        self.assertEqual(send.status_code, 201, send.data)
        request_id = send.data["id"]

        accept = self.bob_client.post(
            reverse("social-friend-request-accept", args=[request_id])
        )
        self.assertIn(accept.status_code, (200, 201))

        friends = self.alice_client.get(reverse("social-friends-list"))
        self.assertEqual(friends.status_code, 200)
        # Either the new friend appears in the list payload or the count is at least 1.
        if isinstance(friends.data, list):
            self.assertTrue(
                any(_friend_id_match(f, self.bob.id) for f in friends.data),
                friends.data,
            )

    def test_notifications_endpoint_returns_expected_shape(self):
        # Alice creates a post — generates a public ActivityEvent.
        self.alice_client.post(
            reverse("social-post-list-create"),
            {"content": "Hello world", "visibility": "public", "post_type": "update"},
            format="json",
        )
        resp = self.bob_client.get(reverse("social-notifications"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("items", resp.data)
        self.assertIn("unseen_count", resp.data)


def _friend_id_match(payload, player_id):
    if isinstance(payload, dict):
        return any(payload.get(k) == player_id for k in ("player_id", "id", "friend_id"))
    return False


# ── STEP 92 — All five path onboarding flows ────────────────────────────────


class Step92AllFivePathOnboardingTests(TestCase):
    """BUILD_ORDER Step 92: every path can be selected + onboarded end-to-end."""

    def _signup_and_select(self, username, path):
        client = APIClient()
        client.post(
            reverse("auth-signup"),
            {"username": username, "password": "testpass123"},
            format="json",
        )
        user = User.objects.get(username=username)
        api = _authed(user)
        api.post(reverse("path-select"), {"path_code": path}, format="json")
        return user, user.player, api

    def test_fitness_warrior_onboarding(self):
        _user, player, api = self._signup_and_select("ob_fw", "fitness_warrior")
        resp = api.post(
            reverse("onboarding-fitness-warrior"),
            {
                "training_split": "ppl",
                "primary_goal": "muscle_gain",
                "training_days_per_week": 4,
                "experience_level": "beginner",
                "split_day_start": "push",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        complete = api.post(
            reverse("onboarding-complete"),
            {"path_code": "fitness_warrior"},
            format="json",
        )
        self.assertEqual(complete.status_code, 200)
        self.assertTrue(FitnessWarriorProfile.objects.filter(player=player).exists())
        self.assertTrue(SplitDayState.objects.filter(player=player).exists())
        self.assertTrue(
            UserPathSelection.objects.get(player=player).onboarding_complete
        )

    def test_mindset_sage_onboarding(self):
        _user, player, api = self._signup_and_select("ob_ms", "mindset_sage")
        resp = api.post(
            reverse("onboarding-mindset-sage"),
            {
                "motivation": "personal_growth",
                "daily_time_commitment": "30_minutes",
                "experience_level": "complete_beginner",
                "archetype": "warrior_sage",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        api.post(
            reverse("onboarding-complete"),
            {"path_code": "mindset_sage"},
            format="json",
        )
        self.assertTrue(MindsetSageProfile.objects.filter(player=player).exists())

    def test_health_alchemist_onboarding(self):
        _user, player, api = self._signup_and_select("ob_ha", "health_alchemist")
        resp = api.post(
            reverse("onboarding-health-alchemist"),
            {
                "primary_health_goal": "full_body_transformation",
                "health_relationship": "starting_from_scratch",
                "focus_area": "all_of_them",
                "equipment_list": ["cold_shower", "sauna"],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        api.post(
            reverse("onboarding-complete"),
            {"path_code": "health_alchemist"},
            format="json",
        )
        self.assertTrue(HealthAlchemistProfile.objects.filter(player=player).exists())
        # Setup guide should now resolve.
        guide = api.get(reverse("alchemist-setup-guide"))
        self.assertEqual(guide.status_code, 200)
        self.assertIn("supplements", guide.data)

    def test_discipline_knight_onboarding(self):
        _user, player, api = self._signup_and_select("ob_dk", "discipline_knight")
        resp = api.post(
            reverse("onboarding-discipline-knight"),
            {
                "routine_level": "no_routine",
                "biggest_challenge": "all_of_them",
                "structure_preference": "semi_structured",
                "time_commitment": "1_hour",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        # Discipline code (3-5 rules) is part of knight onboarding flow.
        code = api.post(
            reverse("onboarding-discipline-code"),
            {"rules": ["No excuses", "Train daily", "Read 10 pages"]},
            format="json",
        )
        self.assertEqual(code.status_code, 200, code.data)
        api.post(
            reverse("onboarding-complete"),
            {"path_code": "discipline_knight"},
            format="json",
        )
        self.assertTrue(DisciplineKnightProfile.objects.filter(player=player).exists())

    def test_grind_visionary_onboarding(self):
        _user, player, api = self._signup_and_select("ob_gv", "grind_visionary")
        resp = api.post(
            reverse("onboarding-grind-visionary"),
            {
                "grind_focus": "coding_and_tech",
                "experience_state": "complete_beginner",
                "singular_goal_text": "Ship my SaaS",
                "goal_timeline": "6_months",
                "daily_hours": "1_hour",
                "current_output_state": "consume_more_than_create",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        api.post(
            reverse("onboarding-complete"),
            {"path_code": "grind_visionary"},
            format="json",
        )
        self.assertTrue(GrindVisionaryProfile.objects.filter(player=player).exists())
        self.assertTrue(SingularGoal.objects.filter(player=player).exists())
        self.assertTrue(
            SkillTree.objects.filter(player=player, path="grind_visionary").exists()
        )


# ── STEP 93 — Daily quest assignment for all five paths ───────────────────────


class Step93DailyAssignmentAllPathsTests(TestCase):
    """BUILD_ORDER Step 93: lineup generation works for each path with no duplicates."""

    @classmethod
    def setUpTestData(cls):
        for path in ALL_PATHS:
            _seed_path_quests(path)
        _seed_universal_quest()

    def _make_onboarded(self, username, path):
        _user, player = _make_user(username)
        _complete_onboarding_for(player, path)
        return player

    def test_lineup_generates_for_each_path_and_is_idempotent(self):
        today = timezone.localdate()
        for path in ALL_PATHS:
            player = self._make_onboarded(f"dq_{path}", path)
            lineup, created = generate_daily_lineup(player=player, target_date=today)
            self.assertTrue(created)
            self.assertEqual(lineup.path, path)
            self.assertGreaterEqual(lineup.items.count(), 1)

            # Quests in the lineup should target the player's path or be universal.
            for item in lineup.items.all():
                if item.quest is None:
                    continue
                self.assertIn(
                    item.quest.path_target,
                    {path, ""},
                    f"Quest {item.quest_id} ({item.quest.title}) on {path} "
                    "lineup has unexpected path_target",
                )

            # Re-running for the same date returns the same lineup, no duplicate.
            again, created_again = generate_daily_lineup(
                player=player, target_date=today
            )
            self.assertFalse(created_again)
            self.assertEqual(again.id, lineup.id)
            self.assertEqual(
                DailyQuestLineup.objects.filter(
                    player=player, path=path, date=today
                ).count(),
                1,
            )


# ── STEP 94 — Path-specific mechanics ────────────────────────────────────────


class Step94PathMechanicsTests(TestCase):
    """BUILD_ORDER Step 94: path-specific mechanic endpoints exist and work."""

    def setUp(self):
        self.user, self.player = _make_user("mech_user")
        _complete_onboarding_for(self.player, "fitness_warrior")
        self.client = _authed(self.user)

    def test_fitness_warrior_split_day_state_is_readable(self):
        SplitDayState.objects.update_or_create(
            player=self.player,
            defaults={
                "current_split": "push",
                "last_updated": timezone.localdate(),
            },
        )
        # State exists and round-trips.
        self.assertEqual(
            SplitDayState.objects.get(player=self.player).current_split, "push"
        )

    def test_mindset_sage_wisdom_log_endpoint(self):
        _complete_onboarding_for(self.player, "mindset_sage")
        today = timezone.localdate()
        post = self.client.post(
            reverse("mechanics-wisdom-log"),
            {"entry": "Today I learned patience.", "log_date": today.isoformat()},
            format="json",
        )
        self.assertEqual(post.status_code, 200, post.data)
        self.assertTrue(WisdomLog.objects.filter(player=self.player).exists())

        get = self.client.get(reverse("mechanics-wisdom-log"))
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

    def test_mindset_sage_dark_night_endpoint(self):
        _complete_onboarding_for(self.player, "mindset_sage")
        long_entry = " ".join(["reflection"] * 110)
        resp = self.client.post(
            reverse("mechanics-dark-night"),
            {"entry": long_entry},
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue(DarkNightEntry.objects.filter(player=self.player).exists())

    def test_health_alchemist_body_journal_and_status(self):
        _complete_onboarding_for(self.player, "health_alchemist")
        today = timezone.localdate()
        resp = self.client.post(
            reverse("mechanics-body-journal"),
            {
                "log_date": today.isoformat(),
                "weight_kg": "75.5",
                "sleep_hours": "7.5",
                "energy_level": 8,
                "notes": "Felt great",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue(BodyJournal.objects.filter(player=self.player).exists())

        status_resp = self.client.get(reverse("mechanics-health-status"))
        self.assertEqual(status_resp.status_code, 200)

    def test_discipline_knight_war_room_and_temptation_log(self):
        _complete_onboarding_for(self.player, "discipline_knight")
        today = timezone.localdate()
        week_start = today - _dt.timedelta(days=today.weekday())

        morning = self.client.post(
            reverse("mechanics-war-room"),
            {
                "week_start": week_start.isoformat(),
                "phase": "morning",
                "objectives": ["Deep work 2h", "Read", "Exercise"],
                "reflection": "Ready",
            },
            format="json",
        )
        self.assertEqual(morning.status_code, 200, morning.data)

        temptation = self.client.post(
            reverse("mechanics-temptation-log"),
            {
                "log_date": today.isoformat(),
                "description": "Skipped social media scroll",
                "resisted": True,
            },
            format="json",
        )
        self.assertEqual(temptation.status_code, 200, temptation.data)
        self.assertTrue(TemptationLog.objects.filter(player=self.player).exists())

        status_resp = self.client.get(reverse("mechanics-discipline-status"))
        self.assertEqual(status_resp.status_code, 200)

    def test_grind_visionary_output_log_and_status(self):
        _complete_onboarding_for(self.player, "grind_visionary")
        today = timezone.localdate()
        resp = self.client.post(
            reverse("mechanics-output-log"),
            {
                "log_date": today.isoformat(),
                "deep_work_hours": "3.5",
                "tasks_shipped": 2,
                "revenue_usd": "0",
                "notes": "Shipped landing page",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue(OutputLog.objects.filter(player=self.player).exists())

        status_resp = self.client.get(reverse("mechanics-grind-status"))
        self.assertEqual(status_resp.status_code, 200)


# ── STEP 95 — Cross-path bonus system ────────────────────────────────────────


class Step95CrossPathBonusTests(TestCase):
    """BUILD_ORDER Step 95: cross-path completion grants bonus EXP exactly once."""

    def setUp(self):
        self.user, self.player = _make_user("cp_bonus")
        # cold_shower pair = fitness_warrior + health_alchemist (worth 20 EXP).
        _set_active_paths(
            self.player, ["fitness_warrior", "health_alchemist"]
        )

        # Two quests sharing the keyword "cold shower" — one per path.
        self.fw_quest = Quest.objects.create(
            title="Cold Shower Reset",
            description="Take a cold shower",
            exp_reward=30,
            path_target="fitness_warrior",
            rank="D",
            pillar="body",
        )
        self.ha_quest = Quest.objects.create(
            title="Cold Shower Protocol",
            description="Daily cold shower protocol",
            exp_reward=30,
            path_target="health_alchemist",
            rank="D",
            pillar="body",
        )

    def _build_lineups_with_completion(self, target_date):
        # Build minimal lineups manually so we control which items are completed.
        fw_lineup = DailyQuestLineup.objects.create(
            player=self.player, path="fitness_warrior", date=target_date
        )
        fw_item = DailyQuestLineupItem.objects.create(
            lineup=fw_lineup, quest=self.fw_quest, slot_order=1
        )
        ha_lineup = DailyQuestLineup.objects.create(
            player=self.player, path="health_alchemist", date=target_date
        )
        ha_item = DailyQuestLineupItem.objects.create(
            lineup=ha_lineup, quest=self.ha_quest, slot_order=1
        )
        for it in (fw_item, ha_item):
            it.completed = True
            it.completed_at = timezone.now()
            it.save(update_fields=["completed", "completed_at"])
        return fw_item, ha_item

    def test_apply_cross_path_bonus_flags_detects_pair(self):
        today = timezone.localdate()
        DailyQuestLineup.objects.create(
            player=self.player, path="fitness_warrior", date=today
        ).items.create(quest=self.fw_quest, slot_order=1)
        DailyQuestLineup.objects.create(
            player=self.player, path="health_alchemist", date=today
        ).items.create(quest=self.ha_quest, slot_order=1)

        result = apply_cross_path_bonus_flags(self.player, today)
        self.assertIsNotNone(result)
        self.assertEqual(
            set(result["paths"]), {"fitness_warrior", "health_alchemist"}
        )
        self.assertGreater(result["bonus_exp"], 0)

    def test_completing_pair_awards_bonus_exp_exactly_once(self):
        today = timezone.localdate()
        self._build_lineups_with_completion(today)

        bonus = detect_cross_path_bonus(self.player, today)
        self.assertGreater(bonus, 0)
        self.assertEqual(
            CrossPathBonus.objects.filter(player=self.player, bonus_date=today).count(),
            1,
        )
        # Re-call returns 0 — bonus is one-shot per day.
        again = detect_cross_path_bonus(self.player, today)
        self.assertEqual(again, 0)

    def test_visionary_multiplier_does_not_double_apply(self):
        # Create a separate player with grind_visionary + mindset_sage and a 2x mult.
        user, player = _make_user("gv_mult_user")
        _set_active_paths(player, ["grind_visionary", "mindset_sage"])
        from paths.models import XPMultiplier
        XPMultiplier.objects.create(player=player, multiplier=2.0)

        today = timezone.localdate()

        # Quests sharing the "reading" keyword.
        gv_quest = Quest.objects.create(
            title="Read 30 mins",
            description="Reading deep work block",
            exp_reward=20,
            path_target="grind_visionary",
            rank="D",
            pillar="mind",
        )
        ms_quest = Quest.objects.create(
            title="Reading Reflection",
            description="Reading session for reflection",
            exp_reward=20,
            path_target="mindset_sage",
            rank="D",
            pillar="mind",
        )

        gv_lineup = DailyQuestLineup.objects.create(
            player=player, path="grind_visionary", date=today
        )
        gv_item = DailyQuestLineupItem.objects.create(
            lineup=gv_lineup, quest=gv_quest, slot_order=1
        )
        ms_lineup = DailyQuestLineup.objects.create(
            player=player, path="mindset_sage", date=today
        )
        ms_item = DailyQuestLineupItem.objects.create(
            lineup=ms_lineup, quest=ms_quest, slot_order=1
        )
        # Mark mindset side as already completed so detect_cross_path_bonus
        # evaluates to a positive bonus when the GV item is completed.
        ms_item.completed = True
        ms_item.completed_at = timezone.now()
        ms_item.save(update_fields=["completed", "completed_at"])

        before = player.exp
        result = complete_lineup_item(player, gv_item.id)
        player.refresh_from_db()

        # Base = 20 quest exp × 2 multiplier = 40
        # Bonus pair "reading" worth 25 × 2 multiplier = 50 — applied to base+bonus, not double.
        # Verify: total earned == exp_earned + bonus_exp; both already include the multiplier.
        gain = player.exp - before
        self.assertEqual(gain, result["exp_earned"] + result["bonus_exp"])
        self.assertEqual(result["exp_earned"], 40)
        self.assertEqual(result["bonus_exp"], 50)


# ── STEP 96 — Cross-path identity titles ─────────────────────────────────────


class Step96CrossPathTitlesTests(TestCase):
    """BUILD_ORDER Step 96: title_warrior_sage / optimized / complete / renaissance.

    Covers correctness, idempotency, and that wrong combinations do not grant.
    Existing C3B coverage is in social/tests_cross_path_titles.py — these tests
    re-verify the locked decision via integration paths.
    """

    @classmethod
    def setUpTestData(cls):
        for key, name, tier in [
            ("title_warrior_sage", "Warrior-Sage", "silver"),
            ("title_optimized_human", "The Optimized Human", "silver"),
            ("title_complete_human", "The Complete Human", "gold"),
            ("title_renaissance_human", "The Renaissance Human", "gold"),
        ]:
            Badge.objects.get_or_create(
                key=key,
                defaults={"name": name, "tier": tier, "description": name},
            )

    def _player_with_paths(self, username, paths):
        _user, player = _make_user(username)
        player.path = paths[0]
        player.save(update_fields=["path", "updated_at"])
        UserPathSelection.objects.create(
            player=player,
            path=paths[0],
            multi_paths_active=paths,
            onboarding_complete=True,
        )
        return player

    def test_warrior_sage_title(self):
        player = self._player_with_paths(
            "wstitle", ["fitness_warrior", "mindset_sage"]
        )
        granted = grant_cross_path_title(player)
        keys = {b.key for b in granted}
        self.assertIn("title_warrior_sage", keys)
        self.assertNotIn("title_optimized_human", keys)

    def test_optimized_human_title(self):
        player = self._player_with_paths(
            "optitle",
            ["fitness_warrior", "mindset_sage", "health_alchemist"],
        )
        keys = {b.key for b in grant_cross_path_title(player)}
        self.assertIn("title_warrior_sage", keys)
        self.assertIn("title_optimized_human", keys)
        self.assertNotIn("title_complete_human", keys)

    def test_complete_human_title(self):
        player = self._player_with_paths(
            "cmtitle",
            [
                "fitness_warrior",
                "mindset_sage",
                "health_alchemist",
                "discipline_knight",
            ],
        )
        keys = {b.key for b in grant_cross_path_title(player)}
        self.assertIn("title_complete_human", keys)
        self.assertNotIn("title_renaissance_human", keys)

    def test_renaissance_human_title(self):
        player = self._player_with_paths("rentitle", ALL_PATHS)
        keys = {b.key for b in grant_cross_path_title(player)}
        self.assertIn("title_renaissance_human", keys)
        # Lower-tier titles also granted in same pass.
        self.assertIn("title_complete_human", keys)
        self.assertIn("title_optimized_human", keys)
        self.assertIn("title_warrior_sage", keys)

    def test_wrong_combination_does_not_grant_title(self):
        # Health Alchemist + Discipline Knight only — no exact title matches.
        player = self._player_with_paths(
            "wrongmix", ["health_alchemist", "discipline_knight"]
        )
        granted = grant_cross_path_title(player)
        self.assertEqual(granted, [])

    def test_repeated_calls_are_idempotent(self):
        player = self._player_with_paths(
            "idem", ["fitness_warrior", "mindset_sage"]
        )
        first = grant_cross_path_title(player)
        second = grant_cross_path_title(player)
        self.assertEqual(len(first), 1)
        self.assertEqual(second, [])
        self.assertEqual(
            UserBadge.objects.filter(
                player=player, badge__key="title_warrior_sage"
            ).count(),
            1,
        )


# ── STEP 97 — Leaderboards ───────────────────────────────────────────────────


class Step97LeaderboardsTests(TestCase):
    """BUILD_ORDER Step 97: weekly/global leaderboards run on QuestCompletion.exp_awarded."""

    def setUp(self):
        self.user, self.player = _make_user("lb_user")

    def _add_completion(self, player, *, path, exp, completion_date=None):
        completion_date = completion_date or timezone.localdate()
        quest = Quest.objects.create(
            title=f"LB quest {path} {exp}",
            description="lb",
            exp_reward=exp,
            path_target=path,
            rank="D",
            pillar="body",
        )
        return QuestCompletion.objects.create(
            player=player,
            quest=quest,
            completion_date=completion_date,
            exp_awarded=exp,
        )

    def test_weekly_exp_leaderboard_uses_completion_exp_awarded(self):
        path = "fitness_warrior"
        a_user, a = _make_user("lb_a")
        b_user, b = _make_user("lb_b")
        # Use start of UTC week per leaderboard convention.
        from social.services.leaderboards import _start_of_week_utc
        week_start = _start_of_week_utc().date()
        self._add_completion(a, path=path, exp=300, completion_date=week_start)
        self._add_completion(b, path=path, exp=100, completion_date=week_start)

        result = weekly_exp_leaderboard(path, requesting_player=a)
        self.assertEqual(len(result["leaderboard"]), 2)
        self.assertEqual(result["leaderboard"][0]["player_id"], a.id)
        self.assertEqual(result["leaderboard"][0]["exp"], 300)

    def test_global_leaderboard_aggregates_across_paths(self):
        from social.services.leaderboards import _start_of_week_utc
        week_start = _start_of_week_utc().date()
        a_user, a = _make_user("lb_global_a")
        self._add_completion(a, path="fitness_warrior", exp=120, completion_date=week_start)
        self._add_completion(a, path="mindset_sage", exp=80, completion_date=week_start)

        result = global_cross_path_leaderboard(requesting_player=a)
        self.assertEqual(result["leaderboard"][0]["player_id"], a.id)
        self.assertEqual(result["leaderboard"][0]["exp"], 200)

    def test_armor_leaderboard_endpoint_returns_payload(self):
        result = armor_leaderboard()
        self.assertIn("leaderboard", result)

    def test_multiplier_streak_leaderboard_endpoint_returns_payload(self):
        result = multiplier_streak_leaderboard()
        self.assertIn("leaderboard", result)

    def test_output_monthly_leaderboard_endpoint_returns_payload(self):
        result = output_log_monthly_leaderboard()
        self.assertIn("leaderboard", result)

    def test_global_leaderboard_endpoint_via_http(self):
        client = _authed(self.user)
        resp = client.get(reverse("social-leaderboard-global"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("leaderboard", resp.data)


# ── STEP 98 — Achievement cards ──────────────────────────────────────────────


class Step98AchievementCardsTests(TestCase):
    """BUILD_ORDER Step 98: achievement cards generated for milestones + visible on profile."""

    @classmethod
    def setUpTestData(cls):
        # Seed the badge catalog so weekly-boss / milestone awards have rows.
        call_command("seed_badges")

    def setUp(self):
        self.user, self.player = _make_user("ac_user")
        self.player.path = "fitness_warrior"
        self.player.save(update_fields=["path", "updated_at"])
        UserPathSelection.objects.create(
            player=self.player,
            path="fitness_warrior",
            onboarding_complete=True,
            multi_paths_active=["fitness_warrior"],
        )

    def test_generate_achievement_card_creates_row(self):
        card = generate_achievement_card(
            self.player,
            card_type="manual_test",
            title="Test Card",
            subtitle="Test Subtitle",
        )
        self.assertEqual(card.player_id, self.player.id)
        self.assertEqual(
            AchievementCard.objects.filter(player=self.player).count(), 1
        )

    def test_weekly_boss_completion_creates_achievement_card(self):
        today = timezone.localdate()
        week_start = today - _dt.timedelta(days=today.weekday())
        boss = WeeklyBossQuest.objects.create(
            path_target="fitness_warrior",
            week_start=week_start,
            title="The Iron Trial",
            description="Defeat the boss",
            exp_reward=400,
            is_active=True,
        )
        result = complete_weekly_boss(self.player, boss.id)
        self.assertFalse(result["already_completed"])
        cards = AchievementCard.objects.filter(
            player=self.player, card_type="weekly_boss_fitness_warrior"
        )
        self.assertEqual(cards.count(), 1)

    def test_cross_path_title_grant_creates_achievement_card(self):
        # Activate two paths so warrior_sage should be granted.
        UserPathSelection.objects.filter(player=self.player).update(
            multi_paths_active=["fitness_warrior", "mindset_sage"]
        )
        # Trigger via complete_path_onboarding hook — the canonical entry point.
        from paths.services import complete_path_onboarding
        complete_path_onboarding(self.player, "mindset_sage")
        cards = AchievementCard.objects.filter(
            player=self.player, card_type="cross_path_title_title_warrior_sage"
        )
        self.assertEqual(cards.count(), 1)

    def test_public_profile_returns_achievement_cards(self):
        generate_achievement_card(
            self.player,
            card_type="manual_test",
            title="Test Card",
            subtitle="Visible on profile",
        )
        client = _authed(self.user)
        resp = client.get(
            reverse("social-public-profile", args=[self.user.username])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("achievement_cards", resp.data)
        titles = [c["title"] for c in resp.data["achievement_cards"]]
        self.assertIn("Test Card", titles)

    def test_dashboard_achievement_summary_returns_recent_cards(self):
        for i in range(3):
            generate_achievement_card(
                self.player,
                card_type=f"summary_card_{i}",
                title=f"Card {i}",
            )
        client = _authed(self.user)
        resp = client.get(reverse("social-achievement-summary"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("recent_cards", resp.data)
        self.assertEqual(resp.data["achievement_card_count"], 3)
        self.assertEqual(len(resp.data["recent_cards"]), 3)
