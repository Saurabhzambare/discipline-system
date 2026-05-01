"""Tests for the leaderboard service and HTTP endpoints."""

from datetime import date, datetime, time, timedelta, timezone as dt_timezone
from decimal import Decimal
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from paths.models import ArmorPiece, OutputLog, XPMultiplier
from players.models import Player
from quests.models import DailyCompletionSummary, Quest, QuestCompletion

from .services.leaderboards import (
    _start_of_week_utc,
    armor_leaderboard,
    global_cross_path_leaderboard,
    multiplier_streak_leaderboard,
    output_log_monthly_leaderboard,
    weekly_exp_leaderboard,
)


User = get_user_model()


def _make_player(username: str, *, path: str = "", streak: int = 0) -> Player:
    user = User.objects.create_user(username=username, password="testpass123")
    player = user.player
    if path:
        player.path = path
    player.streak = streak
    player.save(update_fields=["path", "streak"])
    return player


def _add_completion(
    player: Player,
    *,
    path: str,
    summary_date: date,
    exp: int,
):
    return DailyCompletionSummary.objects.create(
        player=player,
        completion_date=summary_date,
        path=path,
        quests_completed=1,
        quests_total=1,
        total_exp_earned=exp,
        bonus_exp_earned=0,
    )


def _add_completion(player: Player, *, path: str, completion_date: date, exp: int, exp_awarded: int | None = None):
    quest = Quest.objects.create(
        title=f"{player.user.username}-{path}-{completion_date}-{exp}",
        description="leaderboard test quest",
        path_target=path,
        exp_reward=exp,
        rank="D",
        is_active=True,
    )
    return QuestCompletion.objects.create(
        player=player,
        quest=quest,
        completion_date=completion_date,
        exp_awarded=exp if exp_awarded is None else exp_awarded,
    )


class WeeklyExpLeaderboardTests(TestCase):
    def setUp(self):
        self.path = Player.PATH_FITNESS_WARRIOR
        self.week_start = _start_of_week_utc().date()

    def test_empty_state_returns_empty_list(self):
        result = weekly_exp_leaderboard(Player.PATH_FITNESS_WARRIOR)
        self.assertEqual(result["leaderboard"], [])
        self.assertIsNone(result["user_rank"])

    def test_single_player_appears_at_rank_1(self):
        p = _make_player("solo", path=self.path)
        _add_completion(p, path=self.path, completion_date=self.week_start, exp=120)
        result = weekly_exp_leaderboard(self.path, requesting_player=p)
        self.assertEqual(len(result["leaderboard"]), 1)
        self.assertEqual(result["leaderboard"][0]["rank"], 1)
        self.assertEqual(result["leaderboard"][0]["player_id"], p.id)
        self.assertEqual(result["leaderboard"][0]["exp"], 120)
        self.assertEqual(result["user_rank"], 1)

    def test_multiple_players_ordered_correctly(self):
        a = _make_player("alpha", path=self.path)
        b = _make_player("bravo", path=self.path)
        c = _make_player("charlie", path=self.path)
        _add_completion(a, path=self.path, completion_date=self.week_start, exp=50)
        _add_completion(b, path=self.path, completion_date=self.week_start, exp=200)
        _add_completion(c, path=self.path, completion_date=self.week_start, exp=100)

        result = weekly_exp_leaderboard(Player.PATH_FITNESS_WARRIOR)
        ids = [row["player_id"] for row in result["leaderboard"]]
        self.assertEqual(ids, [b.id, c.id, a.id])

    def test_tie_breaker_uses_player_id_ascending(self):
        a = _make_player("aaa", path=self.path)
        b = _make_player("bbb", path=self.path)
        _add_completion(a, path=self.path, completion_date=self.week_start, exp=100)
        _add_completion(b, path=self.path, completion_date=self.week_start, exp=100)

        rows = weekly_exp_leaderboard(self.path)["leaderboard"]
        self.assertEqual(rows[0]["player_id"], a.id)
        self.assertEqual(rows[1]["player_id"], b.id)

    def test_limit_respected(self):
        for i in range(5):
            p = _make_player(f"p{i}", path=self.path)
            _add_completion(p, path=self.path, completion_date=self.week_start, exp=10 * (i + 1))
        result = weekly_exp_leaderboard(self.path, limit=2)
        self.assertEqual(len(result["leaderboard"]), 2)

    def test_user_rank_when_in_top_10(self):
        a = _make_player("a", path=self.path)
        b = _make_player("b", path=self.path)
        _add_completion(a, path=self.path, completion_date=self.week_start, exp=200)
        _add_completion(b, path=self.path, completion_date=self.week_start, exp=100)
        result = weekly_exp_leaderboard(self.path, requesting_player=b)
        self.assertEqual(result["user_rank"], 2)

    def test_user_rank_when_below_top_n(self):
        players = []
        for i in range(11):
            p = _make_player(f"player{i}", path=self.path)
            _add_completion(p, path=self.path, completion_date=self.week_start, exp=1000 - i)
            players.append(p)
        # Last player has the lowest exp -> rank 11
        result = weekly_exp_leaderboard(self.path, limit=5, requesting_player=players[-1])
        self.assertEqual(len(result["leaderboard"]), 5)
        self.assertEqual(result["user_rank"], 11)

    def test_user_rank_null_when_no_qualifying_activity(self):
        a = _make_player("a", path=self.path)
        outsider = _make_player("outsider", path=self.path)
        _add_completion(a, path=self.path, completion_date=self.week_start, exp=50)
        result = weekly_exp_leaderboard(self.path, requesting_player=outsider)
        self.assertIsNone(result["user_rank"])

    def test_previous_week_does_not_contribute(self):
        p = _make_player("p", path=self.path)
        previous_week = self.week_start - timedelta(days=7)
        _add_completion(p, path=self.path, completion_date=previous_week, exp=999)
        result = weekly_exp_leaderboard(Player.PATH_FITNESS_WARRIOR)
        self.assertEqual(result["leaderboard"], [])

    def test_current_week_does_contribute(self):
        p = _make_player("p", path=self.path)
        _add_completion(p, path=self.path, completion_date=self.week_start, exp=42)
        result = weekly_exp_leaderboard(Player.PATH_FITNESS_WARRIOR)
        self.assertEqual(result["leaderboard"][0]["exp"], 42)

    def test_monday_boundary_sunday_excluded_monday_included(self):
        sunday_prev_week = self.week_start - timedelta(days=1)
        p_old = _make_player("old", path=self.path)
        p_new = _make_player("new", path=self.path)
        _add_completion(p_old, path=self.path, completion_date=sunday_prev_week, exp=500)
        _add_completion(p_new, path=self.path, completion_date=self.week_start, exp=10)
        rows = weekly_exp_leaderboard(self.path)["leaderboard"]
        ids = [r["player_id"] for r in rows]
        self.assertEqual(ids, [p_new.id])

    def test_other_path_completions_excluded(self):
        p = _make_player("p", path=self.path)
        _add_completion(p, path=Player.PATH_MINDSET_SAGE, completion_date=self.week_start, exp=999)
        result = weekly_exp_leaderboard(Player.PATH_FITNESS_WARRIOR)
        self.assertEqual(result["leaderboard"], [])


class GlobalCrossPathLeaderboardTests(TestCase):
    def setUp(self):
        self.week_start = _start_of_week_utc().date()

    def test_empty_state(self):
        result = global_cross_path_leaderboard()
        self.assertEqual(result["leaderboard"], [])
        self.assertIsNone(result["user_rank"])

    def test_combines_exp_across_paths(self):
        # DailyCompletionSummary has unique (player, summary_date), so a multi-path
        # player accrues per-day rows on different days; the leaderboard sums them.
        p = _make_player("p", path=Player.PATH_FITNESS_WARRIOR)
        _add_completion(p, path=Player.PATH_FITNESS_WARRIOR, completion_date=self.week_start, exp=100)
        _add_completion(p, path=Player.PATH_MINDSET_SAGE,
                     completion_date=self.week_start + timedelta(days=1), exp=50)
        result = global_cross_path_leaderboard(requesting_player=p)
        self.assertEqual(result["leaderboard"][0]["exp"], 150)
        self.assertEqual(result["user_rank"], 1)

    def test_visionary_stored_exp_already_includes_multiplier(self):
        # Stored summary EXP for a Visionary player already has multiplier baked in.
        v = _make_player("vision", path=Player.PATH_GRIND_VISIONARY)
        normal = _make_player("normal", path=Player.PATH_FITNESS_WARRIOR)
        _add_completion(v, path=Player.PATH_GRIND_VISIONARY, completion_date=self.week_start, exp=300)
        _add_completion(normal, path=Player.PATH_FITNESS_WARRIOR, completion_date=self.week_start, exp=200)
        rows = global_cross_path_leaderboard()["leaderboard"]
        self.assertEqual(rows[0]["player_id"], v.id)
        self.assertEqual(rows[1]["player_id"], normal.id)

    def test_tie_breaker_player_id_ascending(self):
        a = _make_player("a", path=Player.PATH_FITNESS_WARRIOR)
        b = _make_player("b", path=Player.PATH_MINDSET_SAGE)
        _add_completion(a, path=Player.PATH_FITNESS_WARRIOR, completion_date=self.week_start, exp=80)
        _add_completion(b, path=Player.PATH_MINDSET_SAGE, completion_date=self.week_start, exp=80)
        rows = global_cross_path_leaderboard()["leaderboard"]
        self.assertEqual([r["player_id"] for r in rows], [a.id, b.id])

    def test_limit_respected(self):
        for i in range(4):
            p = _make_player(f"g{i}", path=Player.PATH_FITNESS_WARRIOR)
            _add_completion(p, path=Player.PATH_FITNESS_WARRIOR, completion_date=self.week_start, exp=10 * (i + 1))
        result = global_cross_path_leaderboard(limit=2)
        self.assertEqual(len(result["leaderboard"]), 2)


class ArmorLeaderboardTests(TestCase):
    def test_empty_state(self):
        result = armor_leaderboard()
        self.assertEqual(result["leaderboard"], [])
        self.assertIsNone(result["user_rank"])

    def test_only_knights_listed(self):
        knight = _make_player("knight", path=Player.PATH_DISCIPLINE_KNIGHT)
        warrior = _make_player("warrior", path=Player.PATH_FITNESS_WARRIOR)
        ArmorPiece.objects.create(player=knight, slot="boots", name="Iron Boots")
        ArmorPiece.objects.create(player=warrior, slot="helmet", name="Stray Helm")
        rows = armor_leaderboard()["leaderboard"]
        self.assertEqual([r["player_id"] for r in rows], [knight.id])

    def test_gold_prestige_threshold(self):
        gold = _make_player("gold", path=Player.PATH_DISCIPLINE_KNIGHT)
        silver = _make_player("silver", path=Player.PATH_DISCIPLINE_KNIGHT)
        for slot in ["boots", "gauntlets", "chest_plate", "shoulder_guards", "helmet", "shield"]:
            ArmorPiece.objects.create(player=gold, slot=slot, name=f"{slot} g")
        for slot in ["boots", "gauntlets", "chest_plate", "shoulder_guards", "helmet"]:
            ArmorPiece.objects.create(player=silver, slot=slot, name=f"{slot} s")

        rows = armor_leaderboard()["leaderboard"]
        self.assertEqual(rows[0]["player_id"], gold.id)
        self.assertEqual(rows[0]["pieces"], 6)
        self.assertEqual(rows[0]["tier"], "gold_prestige")
        self.assertEqual(rows[1]["player_id"], silver.id)
        self.assertEqual(rows[1]["tier"], "silver")

    def test_tie_breaker(self):
        a = _make_player("aaa", path=Player.PATH_DISCIPLINE_KNIGHT)
        b = _make_player("bbb", path=Player.PATH_DISCIPLINE_KNIGHT)
        ArmorPiece.objects.create(player=a, slot="boots", name="x")
        ArmorPiece.objects.create(player=b, slot="boots", name="y")
        rows = armor_leaderboard()["leaderboard"]
        self.assertEqual([r["player_id"] for r in rows], [a.id, b.id])

    def test_user_rank_when_in_list(self):
        a = _make_player("a", path=Player.PATH_DISCIPLINE_KNIGHT)
        b = _make_player("b", path=Player.PATH_DISCIPLINE_KNIGHT)
        ArmorPiece.objects.create(player=a, slot="boots", name="a1")
        ArmorPiece.objects.create(player=a, slot="helmet", name="a2")
        ArmorPiece.objects.create(player=b, slot="boots", name="b1")
        result = armor_leaderboard(requesting_player=b)
        self.assertEqual(result["user_rank"], 2)

    def test_user_rank_below_top_n(self):
        outsider = _make_player("outsider", path=Player.PATH_DISCIPLINE_KNIGHT)
        ArmorPiece.objects.create(player=outsider, slot="boots", name="z")
        for i in range(3):
            top = _make_player(f"k{i}", path=Player.PATH_DISCIPLINE_KNIGHT)
            ArmorPiece.objects.create(player=top, slot="boots", name=f"a{i}")
            ArmorPiece.objects.create(player=top, slot="helmet", name=f"b{i}")
        result = armor_leaderboard(limit=2, requesting_player=outsider)
        self.assertEqual(len(result["leaderboard"]), 2)
        self.assertEqual(result["user_rank"], 4)

    def test_user_rank_null_when_no_armor(self):
        outsider = _make_player("o", path=Player.PATH_DISCIPLINE_KNIGHT)
        knight = _make_player("k", path=Player.PATH_DISCIPLINE_KNIGHT)
        ArmorPiece.objects.create(player=knight, slot="boots", name="x")
        self.assertIsNone(armor_leaderboard(requesting_player=outsider)["user_rank"])

    def test_limit_respected(self):
        for i in range(4):
            p = _make_player(f"k{i}", path=Player.PATH_DISCIPLINE_KNIGHT)
            ArmorPiece.objects.create(player=p, slot="boots", name=str(i))
        result = armor_leaderboard(limit=2)
        self.assertEqual(len(result["leaderboard"]), 2)


class MultiplierStreakLeaderboardTests(TestCase):
    def _setup_visionary(self, username, *, streak, multiplier):
        p = _make_player(username, path=Player.PATH_GRIND_VISIONARY, streak=streak)
        XPMultiplier.objects.update_or_create(
            player=p,
            defaults={"multiplier": Decimal(str(multiplier))},
        )
        return p

    def test_empty_state(self):
        result = multiplier_streak_leaderboard()
        self.assertEqual(result["leaderboard"], [])
        self.assertIsNone(result["user_rank"])

    def test_only_visionaries_with_active_multiplier(self):
        active = self._setup_visionary("active", streak=5, multiplier=1.5)
        reset = self._setup_visionary("reset", streak=0, multiplier=1.0)
        warrior = _make_player("warrior", path=Player.PATH_FITNESS_WARRIOR, streak=10)
        XPMultiplier.objects.update_or_create(player=warrior, defaults={"multiplier": Decimal("1.5")})
        rows = multiplier_streak_leaderboard()["leaderboard"]
        self.assertEqual([r["player_id"] for r in rows], [active.id])

    def test_ordering_by_streak_days(self):
        a = self._setup_visionary("a", streak=10, multiplier=1.5)
        b = self._setup_visionary("b", streak=20, multiplier=1.7)
        c = self._setup_visionary("c", streak=15, multiplier=1.6)
        rows = multiplier_streak_leaderboard()["leaderboard"]
        ids = [r["player_id"] for r in rows]
        self.assertEqual(ids, [b.id, c.id, a.id])

    def test_tie_breaker_player_id(self):
        a = self._setup_visionary("aaa", streak=12, multiplier=1.5)
        b = self._setup_visionary("bbb", streak=12, multiplier=1.5)
        rows = multiplier_streak_leaderboard()["leaderboard"]
        self.assertEqual([r["player_id"] for r in rows], [a.id, b.id])

    def test_limit_and_user_rank(self):
        players = [self._setup_visionary(f"v{i}", streak=30 - i, multiplier=1.5) for i in range(5)]
        result = multiplier_streak_leaderboard(limit=2, requesting_player=players[-1])
        self.assertEqual(len(result["leaderboard"]), 2)
        self.assertEqual(result["user_rank"], 5)

    def test_user_rank_null_when_no_active_multiplier(self):
        active = self._setup_visionary("active", streak=10, multiplier=1.5)
        outsider = self._setup_visionary("outsider", streak=0, multiplier=1.0)
        result = multiplier_streak_leaderboard(requesting_player=outsider)
        self.assertIsNone(result["user_rank"])


class OutputLogMonthlyLeaderboardTests(TestCase):
    def setUp(self):
        self.month_start = datetime.now(dt_timezone.utc).date().replace(day=1)

    def _add_log(self, player, log_date):
        return OutputLog.objects.create(
            player=player,
            log_date=log_date,
            deep_work_hours=Decimal("1.0"),
            tasks_shipped=1,
        )

    def test_empty_state(self):
        result = output_log_monthly_leaderboard()
        self.assertEqual(result["leaderboard"], [])
        self.assertIsNone(result["user_rank"])

    def test_only_visionaries_listed(self):
        v = _make_player("v", path=Player.PATH_GRIND_VISIONARY)
        warrior = _make_player("w", path=Player.PATH_FITNESS_WARRIOR)
        self._add_log(v, self.month_start)
        self._add_log(warrior, self.month_start)
        rows = output_log_monthly_leaderboard()["leaderboard"]
        self.assertEqual([r["player_id"] for r in rows], [v.id])

    def test_ordering_and_tie_breaker(self):
        a = _make_player("aaa", path=Player.PATH_GRIND_VISIONARY)
        b = _make_player("bbb", path=Player.PATH_GRIND_VISIONARY)
        c = _make_player("ccc", path=Player.PATH_GRIND_VISIONARY)
        # a: 2 logs, b: 2 logs, c: 3 logs
        self._add_log(a, self.month_start)
        self._add_log(a, self.month_start + timedelta(days=1))
        self._add_log(b, self.month_start)
        self._add_log(b, self.month_start + timedelta(days=2))
        self._add_log(c, self.month_start)
        self._add_log(c, self.month_start + timedelta(days=1))
        self._add_log(c, self.month_start + timedelta(days=2))
        rows = output_log_monthly_leaderboard()["leaderboard"]
        self.assertEqual([r["player_id"] for r in rows], [c.id, a.id, b.id])

    def test_previous_month_excluded(self):
        v = _make_player("v", path=Player.PATH_GRIND_VISIONARY)
        last_month = self.month_start - timedelta(days=1)
        self._add_log(v, last_month)
        result = output_log_monthly_leaderboard()
        self.assertEqual(result["leaderboard"], [])

    def test_limit_and_user_rank(self):
        players = []
        for i in range(4):
            p = _make_player(f"v{i}", path=Player.PATH_GRIND_VISIONARY)
            for j in range(i + 1):
                self._add_log(p, self.month_start + timedelta(days=j))
            players.append(p)
        result = output_log_monthly_leaderboard(limit=2, requesting_player=players[0])
        self.assertEqual(len(result["leaderboard"]), 2)
        self.assertEqual(result["user_rank"], 4)

    def test_user_rank_null_when_no_logs(self):
        p_with = _make_player("with", path=Player.PATH_GRIND_VISIONARY)
        p_without = _make_player("without", path=Player.PATH_GRIND_VISIONARY)
        self._add_log(p_with, self.month_start)
        self.assertIsNone(output_log_monthly_leaderboard(requesting_player=p_without)["user_rank"])


class LeaderboardEndpointAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="caller", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.week_start = _start_of_week_utc().date()

    def test_weekly_endpoint_returns_payload(self):
        _add_completion(self.user.player, path=Player.PATH_FITNESS_WARRIOR,
                     completion_date=self.week_start, exp=33)
        url = reverse("social-leaderboard-weekly", args=[Player.PATH_FITNESS_WARRIOR])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("leaderboard", response.data)
        self.assertIn("user_rank", response.data)

    def test_weekly_endpoint_unknown_path(self):
        url = reverse("social-leaderboard-weekly", args=["bogus_path"])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_weekly_endpoint_requires_auth(self):
        anon = APIClient()
        url = reverse("social-leaderboard-weekly", args=[Player.PATH_FITNESS_WARRIOR])
        self.assertEqual(anon.get(url).status_code, 401)

    def test_global_endpoint(self):
        _add_completion(self.user.player, path=Player.PATH_FITNESS_WARRIOR,
                     completion_date=self.week_start, exp=10)
        response = self.client.get(reverse("social-leaderboard-global"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["leaderboard"][0]["player_id"], self.user.player.id)

    def test_armor_endpoint(self):
        self.user.player.path = Player.PATH_DISCIPLINE_KNIGHT
        self.user.player.save(update_fields=["path"])
        ArmorPiece.objects.create(player=self.user.player, slot="boots", name="iron")
        response = self.client.get(reverse("social-leaderboard-armor"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["leaderboard"][0]["tier"], "silver")

    def test_multiplier_streak_endpoint(self):
        self.user.player.path = Player.PATH_GRIND_VISIONARY
        self.user.player.streak = 7
        self.user.player.save(update_fields=["path", "streak"])
        XPMultiplier.objects.create(player=self.user.player, multiplier=Decimal("1.4"))
        response = self.client.get(reverse("social-leaderboard-multiplier-streak"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["leaderboard"][0]["streak_days"], 7)

    def test_output_monthly_endpoint(self):
        self.user.player.path = Player.PATH_GRIND_VISIONARY
        self.user.player.save(update_fields=["path"])
        OutputLog.objects.create(
            player=self.user.player,
            log_date=datetime.now(dt_timezone.utc).date().replace(day=1),
            deep_work_hours=Decimal("1.0"),
            tasks_shipped=2,
        )
        response = self.client.get(reverse("social-leaderboard-output-monthly"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["leaderboard"][0]["output_count"], 1)

    def test_limit_query_param(self):
        # Two summaries, limit=1
        other = User.objects.create_user(username="other", password="testpass123")
        _add_completion(self.user.player, path=Player.PATH_FITNESS_WARRIOR,
                     completion_date=self.week_start, exp=10)
        _add_completion(other.player, path=Player.PATH_FITNESS_WARRIOR,
                     completion_date=self.week_start, exp=20)
        url = reverse("social-leaderboard-weekly", args=[Player.PATH_FITNESS_WARRIOR]) + "?limit=1"
        response = self.client.get(url)
        self.assertEqual(len(response.data["leaderboard"]), 1)

    def test_weekly_uses_exp_awarded_not_quest_base_reward(self):
        p = _make_player("awarded", path=Player.PATH_FITNESS_WARRIOR)
        _add_completion(p, path=Player.PATH_FITNESS_WARRIOR, completion_date=self.week_start, exp=100, exp_awarded=180)
        result = weekly_exp_leaderboard(Player.PATH_FITNESS_WARRIOR)
        self.assertEqual(result["leaderboard"][0]["exp"], 180)


class LeaderboardSourceTests(TestCase):
    def setUp(self):
        self.week_start = _start_of_week_utc().date()

    def test_global_uses_exp_awarded_not_quest_base_reward(self):
        p = _make_player("g_awarded", path=Player.PATH_FITNESS_WARRIOR)
        _add_completion(p, path=Player.PATH_FITNESS_WARRIOR, completion_date=self.week_start, exp=90, exp_awarded=140)
        rows = global_cross_path_leaderboard()["leaderboard"]
        self.assertEqual(rows[0]["exp"], 140)

    def test_weekly_and_global_ignore_daily_completion_summary(self):
        p = _make_player("summary_only", path=Player.PATH_FITNESS_WARRIOR)
        DailyCompletionSummary.objects.create(
            player=p,
            summary_date=self.week_start,
            path=Player.PATH_FITNESS_WARRIOR,
            quests_completed=1,
            quests_total=1,
            total_exp_earned=999,
            bonus_exp_earned=0,
        )
        self.assertEqual(weekly_exp_leaderboard(Player.PATH_FITNESS_WARRIOR)["leaderboard"], [])
        self.assertEqual(global_cross_path_leaderboard()["leaderboard"], [])
