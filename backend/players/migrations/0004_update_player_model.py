# Generated manually — Phase 5B Session 1
#
# This migration does four things:
#
# 1. Updates Player.path choices to the five new Phase 5B paths.
# 2. Adds Player.timezone (used for midnight quest reset per local time).
# 3. Adds Player.last_active_date (used for missed-day detection).
# 4. Recalculates Player.level for all existing records using the new
#    quadratic EXP formula: EXP needed = level² × 50 − 50
#    (replaces old linear formula: level = exp // 100 + 1)
#
# The quadratic formula gives:
#   Level 1  =      0 EXP
#   Level 2  =    150 EXP
#   Level 3  =    400 EXP
#   Level 4  =    750 EXP
#   Level 5  =  1,200 EXP
#   Level 10 =  4,950 EXP
#   Level 20 = 19,950 EXP
#   Level 30 = 44,950 EXP

import math
from django.db import migrations, models


def recalculate_player_levels(apps, schema_editor):
    """
    Recalculate every Player's level using the new quadratic formula.
    Level is the largest L such that L² × 50 − 50 ≤ player.exp.
    Rearranged: L = floor(sqrt((exp + 50) / 50)), minimum 1.
    """
    Player = apps.get_model("players", "Player")
    players_to_update = []

    for player in Player.objects.all():
        new_level = max(1, int(math.sqrt((player.exp + 50) / 50)))
        if new_level != player.level:
            player.level = new_level
            players_to_update.append(player)

    if players_to_update:
        Player.objects.bulk_update(players_to_update, ["level"])


def reverse_recalculate_player_levels(apps, schema_editor):
    """
    Reverse to old linear formula: level = exp // 100 + 1.
    Used only if this migration is reversed (unlikely in production).
    """
    Player = apps.get_model("players", "Player")
    players_to_update = []

    for player in Player.objects.all():
        old_level = (player.exp // 100) + 1
        if old_level != player.level:
            player.level = old_level
            players_to_update.append(player)

    if players_to_update:
        Player.objects.bulk_update(players_to_update, ["level"])


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0003_clear_old_paths"),
    ]

    operations = [
        # 1. Update path field choices to new Phase 5B values.
        migrations.AlterField(
            model_name="player",
            name="path",
            field=models.CharField(
                blank=True,
                choices=[
                    ("fitness_warrior", "Fitness Warrior"),
                    ("mindset_sage", "Mindset Sage"),
                    ("health_alchemist", "Health Alchemist"),
                    ("discipline_knight", "Discipline Knight"),
                    ("grind_visionary", "Grind Visionary"),
                ],
                default="",
                max_length=20,
            ),
        ),
        # 2. Add timezone field — used by midnight quest assignment
        #    scheduler to run at midnight in the player's local time.
        migrations.AddField(
            model_name="player",
            name="timezone",
            field=models.CharField(
                default="UTC",
                max_length=50,
                blank=True,
                help_text=(
                    "Player's local timezone (e.g. 'America/Toronto'). "
                    "Used for midnight quest reset and 9PM end-of-day summary."
                ),
            ),
        ),
        # 3. Add last_active_date — used by missed-day detection logic
        #    to determine if a Grace Token, Streak Shield, or Multiplier
        #    Protection should be applied on login.
        migrations.AddField(
            model_name="player",
            name="last_active_date",
            field=models.DateField(
                null=True,
                blank=True,
                help_text=(
                    "Date of last quest completion. Used to detect "
                    "missed days and trigger protection mechanics."
                ),
            ),
        ),
        # 4. Recalculate all existing Player.level values using the
        #    new quadratic formula. Players with low EXP (< 150) stay
        #    at Level 1. Players who had been bumped to Level 2+ by the
        #    old linear formula may return to Level 1 if they have < 150 EXP.
        migrations.RunPython(
            recalculate_player_levels,
            reverse_code=reverse_recalculate_player_levels,
        ),
    ]
