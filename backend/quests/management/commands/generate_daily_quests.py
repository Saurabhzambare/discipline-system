from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from zoneinfo import ZoneInfo

from paths.models import UserPathSelection
from paths.services import generate_knight_weekly_report
from players.models import Player
from quests.models import DailyQuestLineup
from quests.services import generate_daily_lineup


class Command(BaseCommand):
    help = "Generate pre-computed daily quest lineups (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--player-id", type=int, default=None)
        parser.add_argument("--date", type=str, default=None, help="YYYY-MM-DD")
        parser.add_argument("--force", action="store_true", default=False)

    def handle(self, *args, **options):
        player_id = options["player_id"]
        override_date = date.fromisoformat(options["date"]) if options["date"] else None
        force = options["force"]

        players = Player.objects.filter(path__in=[
            "fitness_warrior", "mindset_sage", "health_alchemist", "discipline_knight", "grind_visionary",
        ]).select_related("user")

        if player_id:
            players = players.filter(id=player_id)

        generated = 0
        skipped = 0
        errors = 0
        touched_timezones = set()

        now_utc = timezone.now()
        for player in players:
            selection = UserPathSelection.objects.filter(player=player, onboarding_complete=True).first()
            if not selection:
                continue
            active_paths = selection.multi_paths_active or [selection.path]

            tz_name = player.timezone or "UTC"
            try:
                tz = ZoneInfo(tz_name)
            except Exception:  # noqa: BLE001
                tz = ZoneInfo("UTC")
            touched_timezones.add(str(tz))
            local_now = now_utc.astimezone(tz)

            # pre-generation mode: only after local midnight or explicit --date
            if not override_date and local_now.hour == 23 and local_now.minute < 30:
                continue

            target_date = override_date or local_now.date()
            for path_code in active_paths:
                try:
                    if not force and DailyQuestLineup.objects.filter(player=player, path=path_code, date=target_date).exists():
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
                    else:
                        skipped += 1
                except Exception as exc:  # noqa: BLE001
                    errors += 1
                    self.stderr.write(self.style.ERROR(f"ERROR player={player.id} path={path_code}: {exc}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Generated {generated} lineups across {len(touched_timezones)} timezones. {skipped} skipped (already existed). {errors} errors."
            )
        )

        # On Sundays, auto-generate Knight Weekly Reports for all active Knight players.
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
                    self.stderr.write(self.style.ERROR(f"ERROR knight weekly report player={knight.id}: {exc}"))
            if knight_reports:
                self.stdout.write(self.style.SUCCESS(f"Generated knight weekly reports for {knight_reports} player(s) at week_start={week_start}"))
