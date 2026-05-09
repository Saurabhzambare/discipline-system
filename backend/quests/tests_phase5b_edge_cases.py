"""
Phase 5B edge-case verification tests (C4-2).

Three concerns covered:

1. Timezone / midnight generation behavior — daily lineup generation respects
   each player's local timezone, not server UTC. Includes a DST-boundary
   regression test.
2. Missed-day protection priority order — Grace Token -> Streak Shield ->
   Multiplier Protection -> Elixir Mercy -> streak break.
3. Duplicate / sequential-concurrent completion safety — repeating a
   completion does not double-award EXP or duplicate QuestCompletion rows.

These tests use the in-memory SQLite test database. True multi-thread
concurrency is not exercised (SQLite + Django test client limitation);
duplicate-completion safety is verified by sequential simulation, with the
underlying unique constraint on QuestCompletion as the production safeguard.
"""

import datetime as _dt
from decimal import Decimal
from unittest import mock
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from paths.mechanics import apply_missed_day_protections
from paths.models import (
    ElixirProgress,
    GraceToken,
    MultiplierProtection,
    StreakShield,
    UserPathSelection,
)
from players.models import Player
from quests.models import (
    DailyQuestLineup,
    DailyQuestLineupItem,
    Quest,
    QuestCompletion,
)
from quests.services import (
    _get_player_local_date,
    complete_lineup_item,
    generate_daily_lineup,
)


User = get_user_model()


# ── shared helpers ──────────────────────────────────────────────────────────


def _make_player(username, *, timezone_name="UTC", path="fitness_warrior"):
    user = User.objects.create_user(username=username, password="testpass123")
    player = user.player
    player.path = path
    player.timezone = timezone_name
    player.save(update_fields=["path", "timezone", "updated_at"])
    UserPathSelection.objects.update_or_create(
        player=player,
        defaults={
            "path": path,
            "onboarding_complete": True,
            "multi_paths_active": [path],
        },
    )
    return player


def _seed_starter_quests(path):
    titles = {
        "fitness_warrior": [
            "Complete 20 Pushups",
            "Walk 5000 Steps",
            "Hit Your Protein Target",
        ],
    }.get(path, [])
    for title in titles:
        Quest.objects.get_or_create(
            title=title,
            defaults={
                "description": f"Starter quest for {path}",
                "exp_reward": 20,
                "path_target": path,
                "rank": "D",
                "pillar": "body",
                "is_active": True,
            },
        )
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


def _utc(dt_obj):
    """Helper: build a tz-aware UTC datetime."""
    return dt_obj.replace(tzinfo=_dt.timezone.utc)


# ── 1. Timezone / midnight generation ───────────────────────────────────────


class Phase5BTimezoneGenerationTests(TestCase):
    """Daily lineup generation respects each player's local timezone."""

    @classmethod
    def setUpTestData(cls):
        _seed_starter_quests("fitness_warrior")

    def setUp(self):
        # Player in Los Angeles (UTC-8 in winter / UTC-7 during DST).
        self.player = _make_player("la_player", timezone_name="America/Los_Angeles")

    def test_local_date_at_2330_pacific_is_previous_calendar_day(self):
        # 2026-03-01 07:30 UTC == 2026-02-28 23:30 Pacific (PST).
        utc_now = _utc(_dt.datetime(2026, 3, 1, 7, 30))
        local_date = _get_player_local_date(self.player, now=utc_now)
        self.assertEqual(local_date, _dt.date(2026, 2, 28))

    def test_generation_at_2330_does_not_create_next_day_lineup_early(self):
        # Pacific local time 2026-02-28 23:30 — still on Feb 28 locally.
        utc_now = _utc(_dt.datetime(2026, 3, 1, 7, 30))
        with mock.patch(
            "quests.services.timezone.now", return_value=utc_now
        ):
            lineup, created = generate_daily_lineup(player=self.player)
            self.assertTrue(created)
            self.assertEqual(lineup.date, _dt.date(2026, 2, 28))

        # No future-date lineup exists.
        self.assertFalse(
            DailyQuestLineup.objects.filter(
                player=self.player, date=_dt.date(2026, 3, 1)
            ).exists()
        )
        self.assertEqual(
            DailyQuestLineup.objects.filter(player=self.player).count(), 1
        )

    def test_generation_at_local_midnight_creates_next_day_lineup(self):
        # 2026-03-01 08:00 UTC == 2026-03-01 00:00 Pacific (PST).
        utc_now = _utc(_dt.datetime(2026, 3, 1, 8, 0))
        with mock.patch(
            "quests.services.timezone.now", return_value=utc_now
        ):
            lineup, created = generate_daily_lineup(player=self.player)
            self.assertTrue(created)
            self.assertEqual(lineup.date, _dt.date(2026, 3, 1))

        # Exactly one lineup for the new local date.
        self.assertEqual(
            DailyQuestLineup.objects.filter(
                player=self.player, date=_dt.date(2026, 3, 1)
            ).count(),
            1,
        )

    def test_same_day_scheduler_re_run_is_idempotent(self):
        utc_now = _utc(_dt.datetime(2026, 3, 1, 8, 0))
        with mock.patch(
            "quests.services.timezone.now", return_value=utc_now
        ):
            first, created_1 = generate_daily_lineup(player=self.player)
            self.assertTrue(created_1)
            second, created_2 = generate_daily_lineup(player=self.player)
            self.assertFalse(created_2)
            self.assertEqual(first.id, second.id)

        self.assertEqual(
            DailyQuestLineup.objects.filter(
                player=self.player, date=_dt.date(2026, 3, 1)
            ).count(),
            1,
        )

    def test_no_extra_lineup_23_hours_into_same_local_day(self):
        # Generate at local midnight, then advance ~23 hours but stay on same local day.
        first_utc = _utc(_dt.datetime(2026, 3, 1, 8, 0))
        later_utc = _utc(_dt.datetime(2026, 3, 2, 7, 30))  # 2026-03-01 23:30 Pacific
        with mock.patch("quests.services.timezone.now", return_value=first_utc):
            generate_daily_lineup(player=self.player)
        with mock.patch("quests.services.timezone.now", return_value=later_utc):
            generate_daily_lineup(player=self.player)

        self.assertEqual(
            DailyQuestLineup.objects.filter(
                player=self.player, date=_dt.date(2026, 3, 1)
            ).count(),
            1,
        )
        self.assertFalse(
            DailyQuestLineup.objects.filter(
                player=self.player, date=_dt.date(2026, 3, 2)
            ).exists()
        )

    def test_next_local_midnight_generates_next_day_lineup(self):
        day1_utc = _utc(_dt.datetime(2026, 3, 1, 8, 0))   # 2026-03-01 00:00 Pacific
        day2_utc = _utc(_dt.datetime(2026, 3, 2, 8, 0))   # 2026-03-02 00:00 Pacific
        with mock.patch("quests.services.timezone.now", return_value=day1_utc):
            generate_daily_lineup(player=self.player)
        with mock.patch("quests.services.timezone.now", return_value=day2_utc):
            generate_daily_lineup(player=self.player)

        self.assertTrue(
            DailyQuestLineup.objects.filter(
                player=self.player, date=_dt.date(2026, 3, 1)
            ).exists()
        )
        self.assertTrue(
            DailyQuestLineup.objects.filter(
                player=self.player, date=_dt.date(2026, 3, 2)
            ).exists()
        )
        self.assertEqual(
            DailyQuestLineup.objects.filter(player=self.player).count(), 2
        )


# ── 2. DST boundary ─────────────────────────────────────────────────────────


class Phase5BDSTGenerationTests(TestCase):
    """Spring-forward DST in America/New_York must not skip or duplicate dates.

    On 2026-03-08 the US shifts from EST (UTC-5) to EDT (UTC-4) at 02:00 local;
    local clocks jump from 01:59:59 -> 03:00:00. The local _calendar date_ is
    not affected — there is still exactly one March 8 — so generation must
    produce one lineup for 2026-03-08 and one for 2026-03-09.
    """

    @classmethod
    def setUpTestData(cls):
        _seed_starter_quests("fitness_warrior")

    def setUp(self):
        self.player = _make_player("ny_player", timezone_name="America/New_York")

    def test_spring_forward_does_not_skip_or_duplicate_local_date(self):
        # Anchor times at midnight local time on each side of the DST jump.
        # 2026-03-08 00:00 EST  -> 2026-03-08 05:00 UTC
        # 2026-03-09 00:00 EDT  -> 2026-03-09 04:00 UTC
        midnight_mar8_utc = _utc(_dt.datetime(2026, 3, 8, 5, 0))
        # A run a few hours into Sunday (after the DST jump):
        post_jump_utc = _utc(_dt.datetime(2026, 3, 8, 14, 0))   # local 10:00 EDT
        midnight_mar9_utc = _utc(_dt.datetime(2026, 3, 9, 4, 0))

        with mock.patch("quests.services.timezone.now", return_value=midnight_mar8_utc):
            d1, created_1 = generate_daily_lineup(player=self.player)
        self.assertTrue(created_1)
        self.assertEqual(d1.date, _dt.date(2026, 3, 8))

        # A second run after the spring-forward jump must be a no-op for the same local date.
        with mock.patch("quests.services.timezone.now", return_value=post_jump_utc):
            d1_again, created_again = generate_daily_lineup(player=self.player)
        self.assertFalse(created_again)
        self.assertEqual(d1_again.id, d1.id)

        with mock.patch("quests.services.timezone.now", return_value=midnight_mar9_utc):
            d2, created_2 = generate_daily_lineup(player=self.player)
        self.assertTrue(created_2)
        self.assertEqual(d2.date, _dt.date(2026, 3, 9))

        # No skipped or duplicated dates.
        dates = sorted(
            DailyQuestLineup.objects.filter(player=self.player).values_list("date", flat=True)
        )
        self.assertEqual(dates, [_dt.date(2026, 3, 8), _dt.date(2026, 3, 9)])

    def test_local_date_helper_stays_correct_across_dst_boundary(self):
        # Just before the spring-forward jump (01:30 EST == 06:30 UTC).
        before = _utc(_dt.datetime(2026, 3, 8, 6, 30))
        # Just after (03:30 EDT == 07:30 UTC).
        after = _utc(_dt.datetime(2026, 3, 8, 7, 30))
        self.assertEqual(_get_player_local_date(self.player, now=before), _dt.date(2026, 3, 8))
        self.assertEqual(_get_player_local_date(self.player, now=after), _dt.date(2026, 3, 8))


# ── 3. Missed-day protection priority order ─────────────────────────────────


class Phase5BMissedDayProtectionOrderTests(TestCase):
    """Verify Grace -> Shield -> Multiplier Protection -> Elixir Mercy -> reset.

    Each test sets player.last_active_date to 3 days ago so apply_missed_day_protections
    sees a real gap (gap > 1) and runs through the priority chain.
    """

    def setUp(self):
        self.today = timezone.localdate()
        self.player = _make_player(
            "missed_day_player", path="fitness_warrior", timezone_name="UTC"
        )
        self.player.streak = 9
        self.player.last_active_date = self.today - _dt.timedelta(days=3)
        self.player.save(update_fields=["streak", "last_active_date", "updated_at"])

    def _add_grace(self):
        return GraceToken.objects.create(
            player=self.player,
            earned_on=self.today - _dt.timedelta(days=10),
            is_used=False,
        )

    def _add_shield(self, count=1):
        return StreakShield.objects.update_or_create(
            player=self.player,
            defaults={"shields_available": count},
        )[0]

    def _add_multiplier_protection(self):
        return MultiplierProtection.objects.create(
            player=self.player,
            earned_on=self.today - _dt.timedelta(days=10),
            is_used=False,
        )

    def _add_elixir_mercy(self, fill_days=4):
        return ElixirProgress.objects.update_or_create(
            player=self.player,
            defaults={
                "elixir_level": 2,
                "current_formula": "energy",
                "fill_days": fill_days,
                "mercy_retained_fill_days": 0,
            },
        )[0]

    def test_all_protections_available_consumes_only_grace_token(self):
        grace = self._add_grace()
        shield = self._add_shield(count=1)
        protection = self._add_multiplier_protection()
        progress = self._add_elixir_mercy(fill_days=4)

        result = apply_missed_day_protections(player=self.player, today=self.today)
        self.assertEqual(result["protected_by"], "grace_token")
        self.assertFalse(result["streak_broken"])

        grace.refresh_from_db()
        shield.refresh_from_db()
        protection.refresh_from_db()
        progress.refresh_from_db()
        self.assertTrue(grace.is_used)
        self.assertEqual(shield.shields_available, 1)
        self.assertFalse(protection.is_used)
        self.assertEqual(progress.fill_days, 4)
        self.assertEqual(progress.mercy_retained_fill_days, 0)

    def test_no_grace_consumes_streak_shield_only(self):
        shield = self._add_shield(count=1)
        protection = self._add_multiplier_protection()
        progress = self._add_elixir_mercy(fill_days=4)

        result = apply_missed_day_protections(player=self.player, today=self.today)
        self.assertEqual(result["protected_by"], "streak_shield")
        self.assertFalse(result["streak_broken"])

        shield.refresh_from_db()
        protection.refresh_from_db()
        progress.refresh_from_db()
        self.assertEqual(shield.shields_available, 0)
        self.assertFalse(protection.is_used)
        self.assertEqual(progress.fill_days, 4)

    def test_only_multiplier_protection_consumed_before_elixir_mercy(self):
        protection = self._add_multiplier_protection()
        progress = self._add_elixir_mercy(fill_days=4)

        result = apply_missed_day_protections(player=self.player, today=self.today)
        self.assertEqual(result["protected_by"], "multiplier_protection")
        self.assertFalse(result["streak_broken"])

        protection.refresh_from_db()
        progress.refresh_from_db()
        self.assertTrue(protection.is_used)
        self.assertEqual(progress.fill_days, 4)
        self.assertEqual(progress.mercy_retained_fill_days, 0)

    def test_only_elixir_mercy_breaks_streak_but_retains_partial_fill(self):
        progress = self._add_elixir_mercy(fill_days=4)

        result = apply_missed_day_protections(player=self.player, today=self.today)
        self.assertEqual(result["protected_by"], "elixir_mercy")
        # Elixir Mercy does NOT prevent streak break — it only retains formula fill.
        self.assertTrue(result["streak_broken"])

        progress.refresh_from_db()
        self.player.refresh_from_db()
        self.assertEqual(progress.fill_days, 2)
        self.assertEqual(progress.mercy_retained_fill_days, 2)
        self.assertEqual(self.player.streak, 1)

    def test_no_protections_resets_streak_to_zero(self):
        result = apply_missed_day_protections(player=self.player, today=self.today)
        self.assertIsNone(result["protected_by"])
        self.assertTrue(result["streak_broken"])

        self.player.refresh_from_db()
        self.assertEqual(self.player.streak, 0)

    def test_multi_day_miss_consumes_only_one_protection(self):
        """A multi-day gap evaluated in one call still consumes at most one protection."""
        self.player.last_active_date = self.today - _dt.timedelta(days=5)
        self.player.save(update_fields=["last_active_date", "updated_at"])

        grace_a = GraceToken.objects.create(
            player=self.player,
            earned_on=self.today - _dt.timedelta(days=20),
            is_used=False,
        )
        grace_b = GraceToken.objects.create(
            player=self.player,
            earned_on=self.today - _dt.timedelta(days=10),
            is_used=False,
        )

        result = apply_missed_day_protections(player=self.player, today=self.today)
        self.assertEqual(result["protected_by"], "grace_token")

        grace_a.refresh_from_db()
        grace_b.refresh_from_db()
        # Older grace consumed (FIFO via earned_on); newer remains.
        self.assertTrue(grace_a.is_used)
        self.assertFalse(grace_b.is_used)
        self.assertEqual(
            GraceToken.objects.filter(player=self.player, is_used=False).count(),
            1,
        )


# ── 4. Concurrency / duplicate completion safety ────────────────────────────


class Phase5BConcurrencyCompletionTests(TestCase):
    """Repeated completion attempts must not double-award EXP or duplicate rows.

    SQLite + Django test client cannot reliably exercise true thread concurrency,
    so this suite simulates two sequential completion calls. Production
    correctness is enforced by:
      - the unique constraint on QuestCompletion (player, quest, completion_date)
      - select_for_update + the early `if item.completed: raise` guard in
        complete_lineup_item
    Both are exercised below.
    """

    def setUp(self):
        self.today = timezone.localdate()
        self.player = _make_player(
            "dup_player", path="fitness_warrior", timezone_name="UTC"
        )
        self.quest = Quest.objects.create(
            title="Concurrency test quest",
            description="dup",
            exp_reward=30,
            path_target="fitness_warrior",
            rank="D",
            pillar="body",
        )
        self.lineup = DailyQuestLineup.objects.create(
            player=self.player, path="fitness_warrior", date=self.today
        )
        self.item = DailyQuestLineupItem.objects.create(
            lineup=self.lineup, quest=self.quest, slot_order=1
        )

    def test_duplicate_completion_does_not_double_award_exp(self):
        starting_exp = self.player.exp

        # First call: success.
        result = complete_lineup_item(self.player, self.item.id)
        self.assertTrue(result["item_completed"])
        self.player.refresh_from_db()
        first_exp = self.player.exp
        self.assertGreater(first_exp, starting_exp)

        # Second call: current contract raises ValueError; document this.
        # (See C4-2 final summary for the contract-mismatch flag.)
        with self.assertRaisesMessage(ValueError, "already completed"):
            complete_lineup_item(self.player, self.item.id)

        # Critical invariant: no double-award and no duplicate completion row.
        self.player.refresh_from_db()
        self.assertEqual(self.player.exp, first_exp)
        self.assertEqual(
            QuestCompletion.objects.filter(
                player=self.player,
                quest=self.quest,
                completion_date=self.today,
            ).count(),
            1,
        )
        self.item.refresh_from_db()
        self.assertTrue(self.item.completed)

    def test_simulated_concurrent_sequential_completions_award_exp_once(self):
        """Two near-simultaneous attempts on the same item produce one row + one award.

        SQLite limitation: Django's TestCase wraps each test in a transaction
        which serializes writes; real concurrency would be exercised in
        TransactionTestCase against a multi-writer DB. The unique constraint
        on QuestCompletion is the production safeguard.
        """
        # Scenario: attempt 1 completes; attempt 2 sees `item.completed=True`
        # and raises before reaching QuestCompletion / EXP code.
        starting_exp = self.player.exp
        first = complete_lineup_item(self.player, self.item.id)
        with self.assertRaises(ValueError):
            complete_lineup_item(self.player, self.item.id)

        self.player.refresh_from_db()
        gain = self.player.exp - starting_exp
        self.assertEqual(gain, first["exp_earned"] + first["bonus_exp"])
        self.assertEqual(
            QuestCompletion.objects.filter(
                player=self.player, quest=self.quest, completion_date=self.today
            ).count(),
            1,
        )

    def test_unique_constraint_blocks_duplicate_quest_completion_row(self):
        """The DB unique constraint is the last line of defence."""
        QuestCompletion.objects.create(
            player=self.player,
            quest=self.quest,
            completion_date=self.today,
            exp_awarded=30,
        )
        from django.db import IntegrityError, transaction

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                QuestCompletion.objects.create(
                    player=self.player,
                    quest=self.quest,
                    completion_date=self.today,
                    exp_awarded=30,
                )

        # Still exactly one row.
        self.assertEqual(
            QuestCompletion.objects.filter(
                player=self.player, quest=self.quest, completion_date=self.today
            ).count(),
            1,
        )
