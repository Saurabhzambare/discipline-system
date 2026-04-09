from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from paths.mechanics import apply_missed_day_protections, apply_post_completion_mechanics, process_dark_night_entry
from paths.models import ArmorPiece, DarkNightEntry, FreedomDayToken, GraceToken, PostFirstDollarChain, UserPathSelection, StreakShield
from paths.services import generate_knight_weekly_report
from quests.models import Quest, QuestCompletion
from quests.services import get_daily_lineup


class Session6MindsetMechanicsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="sage6", password="testpass123")
        self.player = self.user.player
        self.player.path = "mindset_sage"
        self.player.save(update_fields=["path", "updated_at"])

    def test_freedom_token_overflow_awards_bonus_exp(self):
        today = timezone.localdate()
        for i in range(3):
            FreedomDayToken.objects.create(player=self.player, earned_on=today - timedelta(days=i + 1))

        self.player.streak = 7
        self.player.save(update_fields=["streak", "updated_at"])

        result = apply_post_completion_mechanics(player=self.player, lineup_path="mindset_sage", completion_date=today)
        self.assertEqual(result.bonus_exp, 200)
        self.assertEqual(FreedomDayToken.objects.filter(player=self.player, is_used=False).count(), 3)

    def test_dark_night_enforces_once_per_day_and_min_word_count(self):
        today = timezone.localdate()
        with self.assertRaisesMessage(ValueError, "at least 100 words"):
            process_dark_night_entry(player=self.player, entry="too short", entry_date=today)

        entry = "word " * 100
        created = process_dark_night_entry(player=self.player, entry=entry, entry_date=today)
        self.assertEqual(created.exp_awarded, 200)
        self.assertEqual(DarkNightEntry.objects.filter(player=self.player, activated_on=today).count(), 1)

        with self.assertRaisesMessage(ValueError, "once per day"):
            process_dark_night_entry(player=self.player, entry=entry, entry_date=today)


class Session6ProtectionOrderTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="protect6", password="testpass123")
        self.player = self.user.player
        self.player.last_active_date = timezone.localdate() - timedelta(days=3)
        self.player.streak = 9
        self.player.save(update_fields=["last_active_date", "streak", "updated_at"])

    def test_protection_prefers_grace_token_before_shield(self):
        today = timezone.localdate()
        GraceToken.objects.create(player=self.player, earned_on=today - timedelta(days=10), is_used=False)
        StreakShield.objects.create(player=self.player, shields_available=1)

        result = apply_missed_day_protections(player=self.player, today=today)

        self.assertEqual(result["protected_by"], "grace_token")
        self.assertTrue(GraceToken.objects.filter(player=self.player, is_used=True).exists())
        self.assertEqual(StreakShield.objects.get(player=self.player).shields_available, 1)


class Session6FirstDollarAndWarRoomTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="gv6", password="testpass123")
        self.player = self.user.player
        self.player.path = "grind_visionary"
        self.player.streak = 10
        self.player.save(update_fields=["path", "streak", "updated_at"])
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_first_dollar_triggers_only_on_legendary_pack_once(self):
        today = timezone.localdate()
        normal_quest = Quest.objects.create(
            title="Output Log Entry",
            exp_reward=20,
            path_target="grind_visionary",
            rank="D",
            pillar="output",
            pack_id="gv_output_log",
        )
        legendary_quest = Quest.objects.create(
            title="Revenue Action",
            exp_reward=20,
            path_target="grind_visionary",
            rank="B",
            pillar="output",
            pack_id="gv_first_dollar",
        )

        normal = apply_post_completion_mechanics(
            player=self.player,
            lineup_path="grind_visionary",
            completion_date=today,
            quest=normal_quest,
        )
        self.assertEqual(normal.bonus_exp, 0)

        first = apply_post_completion_mechanics(
            player=self.player,
            lineup_path="grind_visionary",
            completion_date=today,
            quest=legendary_quest,
        )
        self.assertGreater(first.bonus_exp, 0)
        chain = PostFirstDollarChain.objects.get(player=self.player)
        self.assertTrue(chain.first_dollar_completed)
        self.assertTrue(chain.chain_unlocked)

        second = apply_post_completion_mechanics(
            player=self.player,
            lineup_path="grind_visionary",
            completion_date=today,
            quest=legendary_quest,
        )
        self.assertEqual(second.bonus_exp, 0)

    def test_post_first_dollar_chain_next_step_is_deterministically_surfaced(self):
        today = timezone.localdate()
        UserPathSelection.objects.create(
            player=self.player,
            path="grind_visionary",
            onboarding_complete=True,
            multi_paths_active=["grind_visionary"],
        )
        UserPathSelection.objects.filter(player=self.player).update(
            committed_at=timezone.now() - timedelta(days=5)
        )
        Quest.objects.create(
            title="Universal Quest",
            exp_reward=10,
            path_target="",
            universal_daily=True,
            rank="D",
            pillar="body",
        )
        Quest.objects.create(
            title="Generate Your First $10",
            exp_reward=250,
            path_target="grind_visionary",
            rank="A",
            pillar="output",
            pack_id="gv_first_dollar_10",
        )
        Quest.objects.create(
            title="Filler Quest",
            exp_reward=20,
            path_target="grind_visionary",
            rank="D",
            pillar="output",
            pack_id="gv_output_log",
        )
        PostFirstDollarChain.objects.create(
            player=self.player,
            first_dollar_completed=True,
            chain_unlocked=True,
            chain_stage=1,
        )

        payload = get_daily_lineup(self.player, target_date=today)
        quest_ids = [item["quest_id"] for item in payload["lineup"]["items"] if item["quest_id"]]
        chain_quest = Quest.objects.get(pack_id="gv_first_dollar_10")
        self.assertIn(chain_quest.id, quest_ids)

    def test_war_room_morning_evening_and_bonus_awards(self):
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        url = reverse("mechanics-war-room")
        today = timezone.localdate().isoformat()

        morning = self.client.post(
            url,
            {"week_start": today, "phase": "morning", "objectives": ["A", "B", "C"]},
            format="json",
        )
        self.assertEqual(morning.status_code, 200)
        self.assertEqual(morning.data["morning_exp_awarded"], 35)
        self.assertEqual(morning.data["bonus_awarded_now"], 0)

        evening = self.client.post(
            url,
            {"week_start": today, "phase": "evening", "reflection": "Done with discipline."},
            format="json",
        )
        self.assertEqual(evening.status_code, 200)
        self.assertEqual(evening.data["evening_exp_awarded"], 35)
        self.assertEqual(evening.data["bonus_awarded_now"], 20)
        self.assertTrue(evening.data["same_day_bonus_awarded"])
        self.assertIn("weekly_report_input", evening.data)

        listing = self.client.get(url)
        self.assertEqual(listing.status_code, 200)
        self.assertGreaterEqual(len(listing.data), 1)
        self.assertIn("weekly_report_input", listing.data[0])

    def test_knight_weekly_report_generation_uses_core_inputs(self):
        self.player.path = "discipline_knight"
        self.player.streak = 12
        self.player.save(update_fields=["path", "streak", "updated_at"])

        week_start = timezone.localdate() - timedelta(days=timezone.localdate().weekday())
        war_room_url = reverse("mechanics-war-room")
        self.client.post(
            war_room_url,
            {"week_start": week_start.isoformat(), "phase": "morning", "objectives": ["Plan"]},
            format="json",
        )
        self.client.post(
            war_room_url,
            {"week_start": week_start.isoformat(), "phase": "evening", "reflection": "Review"},
            format="json",
        )
        quest = Quest.objects.create(
            title="War Room Quest",
            exp_reward=30,
            path_target="discipline_knight",
            rank="D",
            pillar="output",
        )
        QuestCompletion.objects.create(
            player=self.player,
            quest=quest,
            completion_date=week_start,
        )

        report = generate_knight_weekly_report(player=self.player, week_start=week_start)
        self.assertEqual(report.week_start, week_start)
        payload = report.report_payload
        self.assertIn("war_room", payload)
        self.assertIn("armor", payload)
        self.assertIn("streak", payload)
        self.assertIn("pillar_performance", payload)

    def test_knight_weekly_report_endpoint_returns_persisted_payload(self):
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        week_start = timezone.localdate() - timedelta(days=timezone.localdate().weekday())
        generate_knight_weekly_report(player=self.player, week_start=week_start)

        response = self.client.get(
            reverse("mechanics-knight-weekly-report"),
            {"week_start": week_start.isoformat()},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("report_payload", response.data)
        self.assertEqual(str(response.data["week_start"]), week_start.isoformat())

    def test_armor_progression_matches_build_order_and_week_six_grants_two_pieces(self):
        self.player.path = "discipline_knight"
        self.player.save(update_fields=["path", "updated_at"])
        today = timezone.localdate()

        expected = {
            7: {"boots"},
            14: {"gauntlets"},
            21: {"chest_plate"},
            28: {"shoulder_guards"},
            35: {"helmet"},
            42: {"shield", "sword"},
        }

        for streak, expected_slots in expected.items():
            self.player.streak = streak
            self.player.save(update_fields=["streak", "updated_at"])
            apply_post_completion_mechanics(
                player=self.player,
                lineup_path="discipline_knight",
                completion_date=today,
            )
            unlocked = set(
                ArmorPiece.objects.filter(player=self.player).values_list("slot", flat=True)
            )
            self.assertTrue(expected_slots.issubset(unlocked))
