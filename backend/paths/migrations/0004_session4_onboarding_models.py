from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("paths", "0003_questchain"),
    ]

    operations = [
        migrations.CreateModel(
            name="FitnessWarriorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("training_split", models.CharField(default="ppl", max_length=40)),
                ("primary_goal", models.CharField(default="general_performance", max_length=40)),
                ("training_days_per_week", models.PositiveSmallIntegerField(default=4)),
                ("experience_level", models.CharField(default="beginner", max_length=40)),
                ("split_day_start", models.CharField(blank=True, default="", max_length=20)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fitness_warrior_profile",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MindsetSageProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("motivation", models.CharField(default="personal_growth", max_length=60)),
                ("daily_time_commitment", models.CharField(default="30_minutes", max_length=40)),
                ("experience_level", models.CharField(default="complete_beginner", max_length=40)),
                ("archetype", models.CharField(default="warrior_sage", max_length=40)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mindset_sage_profile",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HealthAlchemistProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("primary_health_goal", models.CharField(default="full_body_transformation", max_length=60)),
                ("health_relationship", models.CharField(default="starting_from_scratch", max_length=60)),
                ("focus_area", models.CharField(default="all_of_them", max_length=40)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="health_alchemist_profile",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DisciplineKnightProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("routine_level", models.CharField(default="no_routine", max_length=60)),
                ("biggest_challenge", models.CharField(default="all_of_them", max_length=60)),
                ("structure_preference", models.CharField(default="semi_structured", max_length=60)),
                ("time_commitment", models.CharField(default="1_hour", max_length=30)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discipline_knight_profile",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GrindVisionaryProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("grind_focus", models.CharField(default="coding_and_tech", max_length=40)),
                ("grind_focus_other", models.CharField(blank=True, default="", max_length=80)),
                ("experience_state", models.CharField(default="complete_beginner", max_length=60)),
                ("daily_hours", models.CharField(default="1_hour", max_length=30)),
                ("current_output_state", models.CharField(default="consume_more_than_create", max_length=80)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grind_visionary_profile",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PathOnboardingProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "path",
                    models.CharField(
                        choices=[
                            ("fitness_warrior", "Fitness Warrior"),
                            ("mindset_sage", "Mindset Sage"),
                            ("health_alchemist", "Health Alchemist"),
                            ("discipline_knight", "Discipline Knight"),
                            ("grind_visionary", "Grind Visionary"),
                        ],
                        max_length=30,
                    ),
                ),
                ("current_step", models.CharField(default="start", max_length=40)),
                ("answers_snapshot", models.JSONField(default=dict)),
                ("is_completed", models.BooleanField(default=False)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="onboarding_progress",
                        to="players.player",
                    ),
                ),
            ],
            options={"unique_together": {("player", "path")}},
        ),
    ]
