"""
Management command: seed_quests

Populates the Quest table with a rich set of path-specific and universal quests.
Safe to run multiple times — uses get_or_create on title + path_target.

Usage:
    python manage.py seed_quests
    python manage.py seed_quests --clear   # wipe existing quests first
"""

from django.core.management.base import BaseCommand

from quests.models import Quest

# ---------------------------------------------------------------------------
# Quest definitions
# Each entry: (title, description, category, difficulty, recurrence, exp, path)
# path="" means valid for ALL paths
# ---------------------------------------------------------------------------

UNIVERSAL = [
    (
        "Drink 8 glasses of water",
        "Stay hydrated throughout the day. Track each glass.",
        Quest.CATEGORY_HEALTH, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 10, "",
    ),
    (
        "10-minute mindfulness meditation",
        "Sit quietly and focus on your breath. Use an app or simply silence.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 10, "",
    ),
    (
        "Write in your journal",
        "Reflect on the day: what went well, what didn't, what you'll do differently.",
        Quest.CATEGORY_PRODUCTIVITY, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 10, "",
    ),
    (
        "Get 7–8 hours of sleep",
        "Prioritise recovery. Aim to be in bed on time tonight.",
        Quest.CATEGORY_HEALTH, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 10, "",
    ),
]

RUNNER = [
    (
        "Morning run — 3 km",
        "Lace up and get moving. Pace doesn't matter — just cover the distance.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 20, "runner",
    ),
    (
        "Long run — 10 km",
        "Weekly long run. Go at a comfortable conversational pace.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_HARD, Quest.RECURRENCE_WEEKLY, 60, "runner",
    ),
    (
        "Sprint intervals — 10 × 100 m",
        "Warm up 5 min, then 10 all-out sprints with 90 sec rest between each.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_WEEKDAYS, 35, "runner",
    ),
    (
        "Post-run stretch — 15 minutes",
        "Hip flexors, quads, calves, hamstrings. Don't skip this.",
        Quest.CATEGORY_RECOVERY, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 15, "runner",
    ),
    (
        "Rest day — walk 5,000 steps",
        "Active recovery. Keep the legs moving without beating them up.",
        Quest.CATEGORY_HEALTH, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_WEEKLY, 20, "runner",
    ),
    (
        "Track your pace & distance",
        "Log today's run in a app or notebook. Note how you felt.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 10, "runner",
    ),
]

GYM = [
    (
        "Complete your workout session — 45 min",
        "Show up and put in the work. Push, pull, or legs — whatever is scheduled.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_DAILY, 30, "gym",
    ),
    (
        "Hit your daily protein target",
        "Calculate your target (bodyweight × 1.6–2.2g) and hit it today.",
        Quest.CATEGORY_HEALTH, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 15, "gym",
    ),
    (
        "Log your lifts — progressive overload",
        "Record every set and rep. Add weight or reps compared to last session.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_WEEKDAYS, 25, "gym",
    ),
    (
        "Active recovery — stretch & foam roll",
        "30 minutes of mobility work. Prioritise problem areas.",
        Quest.CATEGORY_RECOVERY, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_WEEKLY, 20, "gym",
    ),
    (
        "Zero junk food today",
        "No ultra-processed food, no takeaway, no sugary drinks. Cook your meals.",
        Quest.CATEGORY_HEALTH, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_DAILY, 25, "gym",
    ),
    (
        "Warm up properly before lifting",
        "5 min cardio + 2 warm-up sets per main movement. No cold lifts.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 10, "gym",
    ),
]

DISCIPLINE = [
    (
        "Cold shower — minimum 2 minutes",
        "No easing in. Step in cold, stay for 2 minutes. Build discomfort tolerance.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_DAILY, 30, "discipline",
    ),
    (
        "Wake up before 6:00 AM",
        "No snooze. Feet on the floor the moment the alarm sounds.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_HARD, Quest.RECURRENCE_DAILY, 40, "discipline",
    ),
    (
        "No social media before noon",
        "Keep your first 4 hours of the day distraction-free and high-output.",
        Quest.CATEGORY_PRODUCTIVITY, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 20, "discipline",
    ),
    (
        "Read for 30 minutes",
        "Physical book or e-reader only. No articles or social posts count.",
        Quest.CATEGORY_PRODUCTIVITY, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 20, "discipline",
    ),
    (
        "Complete your task list before 5 PM",
        "Write your top 3 priorities in the morning. Finish all three by 5 PM.",
        Quest.CATEGORY_PRODUCTIVITY, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_WEEKDAYS, 30, "discipline",
    ),
    (
        "No complaining for the entire day",
        "Notice every complaint and stop it. Reframe problems into solutions.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_HARD, Quest.RECURRENCE_DAILY, 35, "discipline",
    ),
]

TOURNAMENT = [
    (
        "1 hour of deliberate skill practice",
        "Focused, intentional practice on your weakest area. No autopilot.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_HARD, Quest.RECURRENCE_DAILY, 50, "tournament",
    ),
    (
        "Study 2 matches or replays",
        "Analyse opponents or top performers. Write down 3 things you learned.",
        Quest.CATEGORY_PRODUCTIVITY, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_WEEKDAYS, 30, "tournament",
    ),
    (
        "Physical conditioning — 30 min cardio",
        "Run, cycle, or row. Keep your body in shape for peak performance.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_DAILY, 30, "tournament",
    ),
    (
        "Mental warm-up — 10 min visualisation",
        "Close your eyes. Visualise executing your craft perfectly under pressure.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 20, "tournament",
    ),
    (
        "Compete in one ranked / practice match",
        "Get your reps in. Practice under real pressure, not just drills.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_WEEKDAYS, 35, "tournament",
    ),
    (
        "Review your performance — write notes",
        "After competing or practicing, write what you did well and what to fix.",
        Quest.CATEGORY_PRODUCTIVITY, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 20, "tournament",
    ),
]

HARD_75 = [
    (
        "Workout #1 — 45 minutes (any type)",
        "First of two daily workouts. Can be weights, cardio, or sport.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_HARD, Quest.RECURRENCE_DAILY, 45, "75_hard",
    ),
    (
        "Workout #2 — 45 minutes outdoors",
        "Second workout must be outside. No excuses for weather.",
        Quest.CATEGORY_FITNESS, Quest.DIFFICULTY_HARD, Quest.RECURRENCE_DAILY, 45, "75_hard",
    ),
    (
        "Follow your diet — zero cheat meals",
        "Stick to your chosen diet exactly. No alcohol, no cheat meals.",
        Quest.CATEGORY_HEALTH, Quest.DIFFICULTY_HARD, Quest.RECURRENCE_DAILY, 40, "75_hard",
    ),
    (
        "Drink 1 gallon of water (3.8 L)",
        "Track every litre. Start early — it's harder than it sounds.",
        Quest.CATEGORY_HEALTH, Quest.DIFFICULTY_MEDIUM, Quest.RECURRENCE_DAILY, 25, "75_hard",
    ),
    (
        "Read 10 pages of non-fiction",
        "Personal development, business, biography, or self-improvement only.",
        Quest.CATEGORY_PRODUCTIVITY, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 20, "75_hard",
    ),
    (
        "Take your daily progress photo",
        "Same time, same lighting, same pose every day. Track the transformation.",
        Quest.CATEGORY_DISCIPLINE, Quest.DIFFICULTY_EASY, Quest.RECURRENCE_DAILY, 10, "75_hard",
    ),
]

ALL_QUESTS = UNIVERSAL + RUNNER + GYM + DISCIPLINE + TOURNAMENT + HARD_75


class Command(BaseCommand):
    help = "Seed the database with path-specific and universal quests."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing quests before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Quest.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing quests."))

        created_count = 0
        updated_count = 0

        for (title, description, category, difficulty, recurrence, exp_reward, path_target) in ALL_QUESTS:
            quest, created = Quest.objects.update_or_create(
                title=title,
                path_target=path_target,
                defaults={
                    "description": description,
                    "category": category,
                    "difficulty": difficulty,
                    "recurrence": recurrence,
                    "exp_reward": exp_reward,
                    "is_active": True,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {created_count} quests created, {updated_count} updated. "
                f"Total in DB: {Quest.objects.count()}"
            )
        )
