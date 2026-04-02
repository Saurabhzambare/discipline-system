from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0004_wipe_quest_data"),
    ]

    operations = [
        # Update path_target choices to new 5 RPG paths
        migrations.AlterField(
            model_name="quest",
            name="path_target",
            field=models.CharField(
                max_length=30,
                choices=[
                    ("", "All Paths"),
                    ("fitness_warrior", "Fitness Warrior"),
                    ("mindset_sage", "Mindset Sage"),
                    ("health_alchemist", "Health Alchemist"),
                    ("discipline_knight", "Discipline Knight"),
                    ("grind_visionary", "Grind Visionary"),
                ],
                blank=True,
                default="",
            ),
        ),
        # Solo Leveling-style rank: E → S
        migrations.AddField(
            model_name="quest",
            name="rank",
            field=models.CharField(
                max_length=10,
                choices=[
                    ("E", "E"),
                    ("D", "D"),
                    ("C", "C"),
                    ("B", "B"),
                    ("A", "A"),
                    ("S", "S"),
                ],
                default="E",
            ),
        ),
        # Four-pillar system used by the daily assignment algorithm
        migrations.AddField(
            model_name="quest",
            name="pillar",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("body", "Body"),
                    ("mind", "Mind"),
                    ("soul", "Soul"),
                    ("output", "Output"),
                ],
                default="body",
            ),
        ),
        # Groups quests into thematic packs (e.g. "warrior_week_1")
        migrations.AddField(
            model_name="quest",
            name="pack_id",
            field=models.CharField(max_length=50, blank=True, default=""),
        ),
        # Prevents re-assignment until N days have passed since last completion
        migrations.AddField(
            model_name="quest",
            name="cooldown_days",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        # Assigned to every player regardless of path
        migrations.AddField(
            model_name="quest",
            name="universal_daily",
            field=models.BooleanField(default=False),
        ),
        # Only eligible for assignment on rest/recovery days
        migrations.AddField(
            model_name="quest",
            name="is_rest_day_quest",
            field=models.BooleanField(default=False),
        ),
        # One weekly boss quest per player per week
        migrations.AddField(
            model_name="quest",
            name="is_weekly_boss",
            field=models.BooleanField(default=False),
        ),
        # Can be assigned and completed only once ever per player
        migrations.AddField(
            model_name="quest",
            name="is_one_time_only",
            field=models.BooleanField(default=False),
        ),
        # Equipment needed (e.g. "barbell") — filtered via EquipmentProfile
        migrations.AddField(
            model_name="quest",
            name="equipment_required",
            field=models.CharField(max_length=100, blank=True, default=""),
        ),
    ]
