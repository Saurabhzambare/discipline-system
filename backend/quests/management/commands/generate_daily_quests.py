"""
Management command: generate daily quest lineups for all active players.

Usage:
    python manage.py generate_daily_quests
    python manage.py generate_daily_quests --date 2026-04-01

Scheduling (no Celery — use system cron or Railway cron job):
    0 0 * * * python manage.py generate_daily_quests

The command respects each player's timezone field to determine their local "today",
so players in different timezones receive their quests at midnight local time.
"""

from datetime import date

import pytz
from django.core.management.base import BaseCommand
from django.utils import timezone

from players.models import Player
from quests.services import assign_daily_quests


class Command(BaseCommand):
    help = "Generate daily quest lineups for all active players."

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            default=None,
            help="Override assignment date for all players (YYYY-MM-DD). "
                 "Defaults to each player's local today based on their timezone.",
        )

    def handle(self, *args, **options):
        override_date = None
        if options["date"]:
            override_date = date.fromisoformat(options["date"])

        # Only generate quests for players who have committed to a path.
        players = Player.objects.filter(
            path__in=[
                "fitness_warrior",
                "mindset_sage",
                "health_alchemist",
                "discipline_knight",
                "grind_visionary",
            ]
        ).select_related("user")

        total = players.count()
        generated = 0
        skipped = 0
        errors = 0

        self.stdout.write(f"Generating daily quests for {total} player(s)...")

        for player in players:
            try:
                if override_date:
                    assignment_date = override_date
                else:
                    # Resolve each player's local date from their timezone field.
                    # TODO: once five-layer algorithm is complete, this is the correct
                    # entry point — each player gets their quests at their local midnight.
                    tz_name = player.timezone or "UTC"
                    try:
                        tz = pytz.timezone(tz_name)
                    except pytz.exceptions.UnknownTimeZoneError:
                        tz = pytz.UTC
                    assignment_date = timezone.now().astimezone(tz).date()

                # assign_daily_quests is idempotent — safe to call multiple times per day.
                # TODO: replace internal flat eligible-quest logic with five-layer algorithm.
                assign_daily_quests(player=player, date=assignment_date)
                generated += 1

            except Exception as exc:  # noqa: BLE001
                errors += 1
                self.stderr.write(
                    self.style.ERROR(
                        f"  ERROR player={player.user.username} ({player.pk}): {exc}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. generated={generated} skipped={skipped} errors={errors}"
            )
        )
