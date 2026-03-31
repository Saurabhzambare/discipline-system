import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social", "0002_socialgroup_alter_activityevent_related_group_and_more"),
        ("players", "0004_update_player_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "tier",
                    models.CharField(
                        choices=[
                            ("bronze", "Bronze"),
                            ("silver", "Silver"),
                            ("gold", "Gold"),
                            ("platinum", "Platinum"),
                            ("legendary", "Legendary"),
                        ],
                        default="bronze",
                        max_length=10,
                    ),
                ),
                ("path_specific", models.CharField(blank=True, default="", max_length=30)),
                ("icon_name", models.CharField(blank=True, default="", max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserBadge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("earned_at", models.DateTimeField(auto_now_add=True)),
                ("is_featured", models.BooleanField(default=False)),
                (
                    "badge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="earners",
                        to="social.badge",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="badges",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-earned_at"],
                "unique_together": {("player", "badge")},
            },
        ),
        migrations.CreateModel(
            name="AchievementCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
                ("subtitle", models.CharField(blank=True, default="", max_length=255)),
                ("earned_at", models.DateTimeField(auto_now_add=True)),
                ("card_type", models.CharField(blank=True, default="", max_length=30)),
                ("metadata", models.JSONField(default=dict)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="achievement_cards",
                        to="players.player",
                    ),
                ),
            ],
            options={"ordering": ["-earned_at"]},
        ),
        migrations.CreateModel(
            name="WeeklyBossQuest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("path_target", models.CharField(blank=True, default="", max_length=30)),
                ("week_start", models.DateField()),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                ("exp_reward", models.PositiveIntegerField(default=500)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "badge",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="boss_quests",
                        to="social.badge",
                    ),
                ),
            ],
            options={
                "ordering": ["-week_start"],
                "unique_together": {("path_target", "week_start")},
            },
        ),
        migrations.CreateModel(
            name="WeeklyBossCompletion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                ("exp_awarded", models.PositiveIntegerField(default=0)),
                (
                    "boss",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="completions",
                        to="social.weeklybossquest",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="boss_completions",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-completed_at"],
                "unique_together": {("player", "boss")},
            },
        ),
    ]
