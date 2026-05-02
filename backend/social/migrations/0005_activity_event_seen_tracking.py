# Generated for C3C — ActivityEvent expansion + per-user read tracking.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0005_alter_player_last_active_date_alter_player_timezone"),
        ("social", "0004_alter_achievementcard_id_alter_badge_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activityevent",
            name="event_type",
            field=models.CharField(
                choices=[
                    ("post_created", "Post Created"),
                    ("friend_added", "Friend Added"),
                    ("joined_group", "Joined Group"),
                    ("quest_completed", "Quest Completed"),
                    ("level_up", "Level Up"),
                    ("multiplier_upgrade", "Multiplier Upgrade"),
                    ("streak_milestone", "Streak Milestone"),
                    ("badge_earned", "Badge Earned"),
                    ("cross_path_title_earned", "Cross-Path Title Earned"),
                    ("partner_quest_completed", "Partner Quest Completed"),
                    ("partner_level_up", "Partner Level Up"),
                    ("first_dollar", "First Dollar"),
                    ("weekly_boss_defeated", "Weekly Boss Defeated"),
                ],
                max_length=30,
            ),
        ),
        migrations.CreateModel(
            name="ActivityEventRead",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seen_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reads",
                        to="social.activityevent",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activity_event_reads",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("event", "player"),
                        name="social_activity_event_read_unique",
                    )
                ],
            },
        ),
    ]
