"""
C3A — Weekly Boss endpoint tests.

GET  /api/quests/weekly-boss/
POST /api/quests/weekly-boss/complete/
"""
import datetime as _dt

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from paths.models import UserPathSelection, XPMultiplier
from players.models import Player
from social.models import (
    AchievementCard,
    Badge,
    UserBadge,
    WeeklyBossCompletion,
    WeeklyBossQuest,
)

User = get_user_model()


def _current_monday():
    today = timezone.localdate()
    return today - _dt.timedelta(days=today.weekday())


def _make_player(username, path="fitness_warrior", exp=0, level=1):
    user = User.objects.create_user(username, password="testpass")
    player = Player.objects.get(user=user)
    player.path = path
    player.exp = exp
    player.level = level
    player.save(update_fields=["path", "exp", "level", "updated_at"])
    # Refresh user so the cached reverse OneToOne (user.player) is cleared.
    user.refresh_from_db()
    return player, user


def _make_boss(path_target="fitness_warrior", exp_reward=400, week_start=None, is_active=True,
               title="Boss Trial"):
    return WeeklyBossQuest.objects.create(
        path_target=path_target,
        week_start=week_start or _current_monday(),
        title=title,
        description="Defeat the weekly boss!",
        exp_reward=exp_reward,
        is_active=is_active,
    )


def _make_badge(key, tier="bronze"):
    badge, _ = Badge.objects.get_or_create(
        key=key,
        defaults={"name": key, "tier": tier, "path_specific": "", "icon_name": ""},
    )
    return badge


def _authed_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# ── GET /api/quests/weekly-boss/ ──────────────────────────────────────────────


class WeeklyBossGetTests(TestCase):

    def test_auth_required(self):
        resp = APIClient().get("/api/quests/weekly-boss/")
        self.assertEqual(resp.status_code, 401)

    def test_empty_bosses_when_none_exist(self):
        player, user = _make_player("wb_get1")
        client = _authed_client(user)
        resp = client.get("/api/quests/weekly-boss/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["bosses"], [])
        self.assertIn("week_start", data)
        self.assertIn("week_end", data)

    def test_returns_boss_for_active_path(self):
        player, user = _make_player("wb_get2", path="fitness_warrior")
        _make_boss(path_target="fitness_warrior", exp_reward=500)
        client = _authed_client(user)
        resp = client.get("/api/quests/weekly-boss/")
        self.assertEqual(resp.status_code, 200)
        bosses = resp.json()["bosses"]
        self.assertEqual(len(bosses), 1)
        self.assertEqual(bosses[0]["path"], "fitness_warrior")
        self.assertEqual(bosses[0]["exp_reward"], 500)
        self.assertEqual(bosses[0]["state"], "available")
        self.assertIsNone(bosses[0]["completion"])

    def test_does_not_return_boss_for_inactive_path(self):
        player, user = _make_player("wb_get3", path="mindset_sage")
        _make_boss(path_target="fitness_warrior")
        client = _authed_client(user)
        resp = client.get("/api/quests/weekly-boss/")
        bosses = resp.json()["bosses"]
        self.assertEqual(len(bosses), 0)

    def test_state_completed_when_completion_exists(self):
        player, user = _make_player("wb_get4", path="fitness_warrior")
        boss = _make_boss(path_target="fitness_warrior", exp_reward=300)
        WeeklyBossCompletion.objects.create(player=player, boss=boss, exp_awarded=300)
        client = _authed_client(user)
        resp = client.get("/api/quests/weekly-boss/")
        bosses = resp.json()["bosses"]
        self.assertEqual(len(bosses), 1)
        self.assertEqual(bosses[0]["state"], "completed")
        self.assertIsNotNone(bosses[0]["completion"])
        self.assertEqual(bosses[0]["completion"]["exp_awarded"], 300)

    def test_multi_path_returns_multiple_bosses(self):
        player, user = _make_player("wb_get5", path="fitness_warrior")
        UserPathSelection.objects.create(
            player=player, path="fitness_warrior", onboarding_complete=True,
            multi_paths_active=["fitness_warrior", "mindset_sage"],
        )
        _make_boss(path_target="fitness_warrior", title="FW Boss")
        _make_boss(path_target="mindset_sage", title="MS Boss")
        client = _authed_client(user)
        resp = client.get("/api/quests/weekly-boss/")
        bosses = resp.json()["bosses"]
        self.assertEqual(len(bosses), 2)
        paths_returned = {b["path"] for b in bosses}
        self.assertEqual(paths_returned, {"fitness_warrior", "mindset_sage"})

    def test_does_not_return_boss_from_different_week(self):
        player, user = _make_player("wb_get6", path="fitness_warrior")
        last_monday = _current_monday() - _dt.timedelta(days=7)
        _make_boss(path_target="fitness_warrior", week_start=last_monday)
        client = _authed_client(user)
        resp = client.get("/api/quests/weekly-boss/")
        bosses = resp.json()["bosses"]
        self.assertEqual(len(bosses), 0)

    def test_returns_all_path_boss(self):
        """A boss with path_target='' should be visible to any player."""
        player, user = _make_player("wb_get7", path="discipline_knight")
        _make_boss(path_target="", title="Global Boss")
        client = _authed_client(user)
        resp = client.get("/api/quests/weekly-boss/")
        bosses = resp.json()["bosses"]
        self.assertEqual(len(bosses), 1)
        self.assertEqual(bosses[0]["title"], "Global Boss")


# ── POST /api/quests/weekly-boss/complete/ ────────────────────────────────────


class WeeklyBossCompleteTests(TestCase):

    def setUp(self):
        _make_badge("fw_boss_week_1", "silver")
        _make_badge("boss_slayer_first", "bronze")
        _make_badge("boss_slayer_5", "silver")
        _make_badge("boss_slayer_10", "gold")

    def test_auth_required(self):
        resp = APIClient().post("/api/quests/weekly-boss/complete/", {"boss_id": 1})
        self.assertEqual(resp.status_code, 401)

    def test_completes_boss_and_awards_exp(self):
        player, user = _make_player("wb_post1", path="fitness_warrior", exp=100)
        boss = _make_boss(path_target="fitness_warrior", exp_reward=400)
        client = _authed_client(user)
        resp = client.post(
            "/api/quests/weekly-boss/complete/",
            {"boss_id": boss.id},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["exp_awarded"], 400)
        self.assertIn("completion", data)
        player.refresh_from_db()
        self.assertEqual(player.exp, 500)

    def test_duplicate_completion_returns_409(self):
        player, user = _make_player("wb_post2", path="fitness_warrior")
        boss = _make_boss(path_target="fitness_warrior", exp_reward=300)
        client = _authed_client(user)
        client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        resp2 = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp2.status_code, 409)

    def test_rejects_boss_from_different_path(self):
        player, user = _make_player("wb_post3", path="mindset_sage")
        boss = _make_boss(path_target="fitness_warrior", exp_reward=300)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("not active on", resp.json()["detail"])

    def test_rejects_expired_boss(self):
        player, user = _make_player("wb_post4", path="fitness_warrior")
        last_monday = _current_monday() - _dt.timedelta(days=7)
        boss = _make_boss(path_target="fitness_warrior", week_start=last_monday)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("not available in the current week", resp.json()["detail"])

    def test_visionary_multiplier_applied(self):
        player, user = _make_player("wb_post5", path="grind_visionary", exp=0)
        _make_badge("gv_boss_week_1", "silver")
        XPMultiplier.objects.create(player=player, multiplier=1.5)
        boss = _make_boss(path_target="grind_visionary", exp_reward=200)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["exp_awarded"], 300)  # 200 * 1.5
        player.refresh_from_db()
        self.assertEqual(player.exp, 300)

    def test_non_visionary_no_multiplier(self):
        player, user = _make_player("wb_post6", path="fitness_warrior", exp=0)
        boss = _make_boss(path_target="fitness_warrior", exp_reward=200)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["exp_awarded"], 200)

    def test_awards_badge(self):
        player, user = _make_player("wb_post7", path="fitness_warrior")
        boss = _make_boss(path_target="fitness_warrior", exp_reward=100)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("fw_boss_week_1", data.get("badges_earned", []))
        self.assertIn("boss_slayer_first", data.get("badges_earned", []))

    def test_creates_achievement_card(self):
        player, user = _make_player("wb_post8", path="fitness_warrior")
        boss = _make_boss(path_target="fitness_warrior", exp_reward=100)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 200)
        card_id = resp.json().get("achievement_card_id")
        self.assertIsNotNone(card_id)
        card = AchievementCard.objects.get(id=card_id)
        self.assertEqual(card.card_type, "weekly_boss_fitness_warrior")

    def test_nonexistent_boss_returns_404(self):
        player, user = _make_player("wb_post9", path="fitness_warrior")
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": 99999}, format="json")
        self.assertEqual(resp.status_code, 404)

    def test_missing_boss_id_returns_400(self):
        player, user = _make_player("wb_post10", path="fitness_warrior")
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {}, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_inactive_boss_returns_404(self):
        player, user = _make_player("wb_post11", path="fitness_warrior")
        boss = _make_boss(path_target="fitness_warrior", is_active=False)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 404)

    def test_level_up_field_returned(self):
        """Player at 1195 EXP (Level 4); boss awards 200 → Level 5."""
        _make_badge("level_5", "bronze")
        player, user = _make_player("wb_post12", path="fitness_warrior", exp=1195, level=4)
        boss = _make_boss(path_target="fitness_warrior", exp_reward=200)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["level_up"])
        self.assertEqual(data["player_level"], 5)

    def test_multi_path_player_can_complete_secondary_boss(self):
        player, user = _make_player("wb_post13", path="fitness_warrior")
        UserPathSelection.objects.create(
            player=player, path="fitness_warrior", onboarding_complete=True,
            multi_paths_active=["fitness_warrior", "mindset_sage"],
        )
        _make_badge("ms_boss_week_1", "silver")
        boss = _make_boss(path_target="mindset_sage", exp_reward=300)
        client = _authed_client(user)
        resp = client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["exp_awarded"], 300)

    def test_completion_record_stored(self):
        player, user = _make_player("wb_post14", path="fitness_warrior")
        boss = _make_boss(path_target="fitness_warrior", exp_reward=250)
        client = _authed_client(user)
        client.post("/api/quests/weekly-boss/complete/", {"boss_id": boss.id}, format="json")
        self.assertTrue(WeeklyBossCompletion.objects.filter(player=player, boss=boss).exists())
        comp = WeeklyBossCompletion.objects.get(player=player, boss=boss)
        self.assertEqual(comp.exp_awarded, 250)
