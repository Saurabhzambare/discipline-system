from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from players.models import Player
from paths.services import generate_knight_weekly_report


class Command(BaseCommand):
    help = "Generate Discipline Knight weekly reports (cron-friendly)."

    def add_arguments(self, parser):
        parser.add_argument("--week-start", type=str, help="Week start date (YYYY-MM-DD). Defaults to current week Monday.")

    def handle(self, *args, **options):
        if options.get("week_start"):
            week_start = timezone.datetime.fromisoformat(options["week_start"]).date()
        else:
            today = timezone.localdate()
            week_start = today - timedelta(days=today.weekday())

        players = Player.objects.filter(path="discipline_knight")
        created = 0
        for player in players.iterator():
            generate_knight_weekly_report(player=player, week_start=week_start)
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Generated knight weekly reports for {created} player(s) at week_start={week_start}"))
