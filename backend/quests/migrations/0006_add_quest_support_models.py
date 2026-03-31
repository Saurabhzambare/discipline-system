import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0005_update_quest_model"),
        ("players", "0004_update_player_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyQuestLineup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("lineup_date", models.DateField()),
                ("quest_ids", models.JSONField(default=list)),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_lineups",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-lineup_date"],
                "unique_together": {("player", "lineup_date")},
            },
        ),
        migrations.CreateModel(
            name="QuestFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "rating",
                    models.CharField(
                        choices=[("up", "Up"), ("down", "Down")],
                        max_length=4,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quest_feedback",
                        to="players.player",
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedback",
                        to="quests.quest",
                    ),
                ),
            ],
            options={"unique_together": {("player", "quest")}},
        ),
        migrations.CreateModel(
            name="QuestPreference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("weight", models.FloatField(default=1.0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quest_preferences",
                        to="players.player",
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preferences",
                        to="quests.quest",
                    ),
                ),
            ],
            options={"unique_together": {("player", "quest")}},
        ),
        migrations.CreateModel(
            name="DailyIntention",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("intention_date", models.DateField()),
                ("text", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_intentions",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-intention_date"],
                "unique_together": {("player", "intention_date")},
            },
        ),
        migrations.CreateModel(
            name="DailySwap",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("swap_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_swaps",
                        to="players.player",
                    ),
                ),
                (
                    "quest_removed",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="swapped_out",
                        to="quests.quest",
                    ),
                ),
                (
                    "quest_added",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="swapped_in",
                        to="quests.quest",
                    ),
                ),
            ],
            options={"ordering": ["-swap_date"]},
        ),
        migrations.CreateModel(
            name="CrossPathBonus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("bonus_date", models.DateField()),
                ("pillars_completed", models.JSONField(default=list)),
                ("bonus_exp", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cross_path_bonuses",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-bonus_date"],
                "unique_together": {("player", "bonus_date")},
            },
        ),
        migrations.CreateModel(
            name="DailyCompletionSummary",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("summary_date", models.DateField()),
                ("quests_completed", models.PositiveSmallIntegerField(default=0)),
                ("total_exp_earned", models.PositiveIntegerField(default=0)),
                ("streak_maintained", models.BooleanField(default=True)),
                ("cross_path_bonus_earned", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_summaries",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-summary_date"],
                "unique_together": {("player", "summary_date")},
            },
        ),
    ]
