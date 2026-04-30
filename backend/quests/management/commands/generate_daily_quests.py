from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from zoneinfo import ZoneInfo

from paths.models import UserPathSelection
from paths.services import generate_knight_weekly_report
from players.models import Player
from quests.models import DailyQuestLineup
from quests.services import apply_cross_path_bonus_flags, generate_daily_lineup


# Cron is expected to fire every 15 minutes; only generate for timezones
# where local time is currently in the midnight window [00:00, MIDNIGHT_WINDOW_MINUTES).
MIDNIGHT_WINDOW_MINUTES = 15


class Command(BaseCommand):
    help = (
        "Generate pre-computed daily quest lineups, idempotently, in each "
        "player's local timezone. By default only generates for timezones "
        "currently inside the midnight window. Pass --force or --date to bypass."
    )

    def add_arguments(self, parser):
        parser.add_argument("--player-id", type=int, default=None,
                            help="Generate for one specific player (bypasses midnight window).")
        parser.add_argument("--date", type=str, default=None,
                            help="YYYY-MM-DD; generate for explicit date (bypasses midnight window).")
        parser.add_argument("--force", action="store_true", default=False,
                            help="Regenerate existing lineups; bypasses midnight window.")
        parser.add_argument("--all-timezones", action="store_true", default=False,
                            help="Bypass midnight window check (still idempotent unless --force).")

    def handle(self, *args, **options):
        player_id = options["player_id"]
        override_date = date.fromisoformat(options["date"]) if options["date"] else None
        force = options["force"]
        all_timezones = options["all_timezones"] or bool(player_id) or bool(override_date) or force

        now_utc = timezone.now()

        eligible_players = Player.objects.filter(path__in=[
            "fitness_warrior", "mindset_sage", "health_alchemist",
            "discipline_knight", "grind_visionary",
        ]).select_related("user")

        if player_id:
            eligible_players = eligible_players.filter(id=player_id)

        # Group players by timezone string (treat empty/None as UTC) so we can
        # check the midnight window once per timezone instead of per player.
        timezones: dict[str, list[Player]] = {}
        for p in eligible_players:
            tz_name = p.timezone or "UTC"
            timezones.setdefault(tz_name, []).append(p)

        generated = 0
        skipped = 0
        errors = 0
        skipped_tz = 0
        touched_timezones: set[str] = set()
        cross_path_pairs_flagged = 0

        for tz_name, players in timezones.items():
            try:
                tz = ZoneInfo(tz_name)
            except Exception:  # noqa: BLE001
                tz = ZoneInfo("UTC")
            local_now = now_utc.astimezone(tz)

            # Midnight-window gate (skip whole timezone if outside the window).
            in_midnight_window = (local_now.hour == 0 and local_now.minute < MIDNIGHT_WINDOW_MINUTES)
            if not all_timezones and not in_midnight_window:
                skipped_tz += 1
                continue

            touched_timezones.add(tz_name)
            target_date = override_date or local_now.date()

            for player in players:
                selection = UserPathSelection.objects.filter(player=player, onboarding_complete=True).first()
                if not selection:
                    continue
                active_paths = selection.multi_paths_active or [selection.path]

                generated_for_player = False
                for path_code in active_paths:
                    try:
                        if not force and DailyQuestLineup.objects.filter(
                            player=player, path=path_code, date=target_date
                        ).exists():
                            skipped += 1
                            continue
                        _, created = generate_daily_lineup(
                            player=player,
                            target_date=target_date,
                            path_code=path_code,
                            force=force,
                        )
                        if created:
                            generated += 1
                            generated_for_player = True
                        else:
                            skipped += 1
                    except Exception as exc:  # noqa: BLE001
                        errors += 1
                        self.stderr.write(self.style.ERROR(
                            f"ERROR player={player.id} path={path_code}: {exc}"
                        ))

                # After all of this player's paths are generated for the day,
                # flag any cross-path bonus pair (max one per day).
                if generated_for_player and len(active_paths) >= 2:
                    try:
                        result = apply_cross_path_bonus_flags(player=player, target_date=target_date)
                        if result:
                            cross_path_pairs_flagged += 1
                    except Exception as exc:  # noqa: BLE001
                        self.stderr.write(self.style.WARNING(
                            f"cross-path flag failed player={player.id}: {exc}"
                        ))

        self.stdout.write(self.style.SUCCESS(
            f"Generated {generated} lineups across {len(touched_timezones)} timezones. "
            f"{skipped} skipped (already existed). {skipped_tz} timezones outside midnight window. "
            f"{cross_path_pairs_flagged} cross-path pairs flagged. {errors} errors."
        ))

        # On Sundays, auto-generate Knight Weekly Reports for all active Knight players.
        # Use UTC date as a simple gate; this matches the previous behavior.
        today = override_date or timezone.localdate()
        if today.weekday() == 6:
            week_start = today - timedelta(days=6)
            knight_players = Player.objects.filter(path="discipline_knight")
            knight_reports = 0
            for knight in knight_players.iterator():
                try:
                    generate_knight_weekly_report(player=knight, week_start=week_start)
                    knight_reports += 1
                except Exception as exc:  # noqa: BLE001
                    self.stderr.write(self.style.ERROR(
                        f"ERROR knight weekly report player={knight.id}: {exc}"
                    ))
            if knight_reports:
                self.stdout.write(self.style.SUCCESS(
                    f"Generated knight weekly reports for {knight_reports} player(s) at week_start={week_start}"
                ))
