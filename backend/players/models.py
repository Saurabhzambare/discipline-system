"""
models.py

This file defines the Player model, which represents the
game profile attached to each user in the Discipline System.
"""

from django.conf import settings
from django.db import models


class Player(models.Model):
    """
    Player model = the "game profile" for a user.

    In the Discipline System:
        User   → authentication identity (login)
        Player → game stats (level, EXP, streak, path)

    EXP formula (quadratic):
        EXP needed to reach level L = L² × 50 − 50
        Level 1 = 0 EXP, Level 2 = 150 EXP, Level 5 = 1200 EXP
        See quests/services.py for calculate_level_from_exp()
    """

    PATH_FITNESS_WARRIOR = "fitness_warrior"
    PATH_MINDSET_SAGE = "mindset_sage"
    PATH_HEALTH_ALCHEMIST = "health_alchemist"
    PATH_DISCIPLINE_KNIGHT = "discipline_knight"
    PATH_GRIND_VISIONARY = "grind_visionary"

    PATH_CHOICES = [
        (PATH_FITNESS_WARRIOR, "Fitness Warrior"),
        (PATH_MINDSET_SAGE, "Mindset Sage"),
        (PATH_HEALTH_ALCHEMIST, "Health Alchemist"),
        (PATH_DISCIPLINE_KNIGHT, "Discipline Knight"),
        (PATH_GRIND_VISIONARY, "Grind Visionary"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="player",
    )

    level = models.PositiveIntegerField(default=1)
    exp = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)

    # Primary path — set after Path Discovery Quiz.
    # Empty string means player has not yet completed onboarding.
    # Multi-path support tracked in paths.UserPathSelection.
    path = models.CharField(max_length=20, choices=PATH_CHOICES, blank=True, default="")

    # Player's local timezone string (e.g. 'America/Toronto').
    # Used by the midnight quest scheduler and 9PM end-of-day summary.
    timezone = models.CharField(max_length=50, default="UTC", blank=True)

    # Date of last quest completion. Used by missed-day detection to
    # trigger Grace Token, Streak Shield, or Multiplier Protection.
    last_active_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Player({self.user.username})"
