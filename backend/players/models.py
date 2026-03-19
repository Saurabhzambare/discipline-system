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
    """

    PATH_RUNNER = "runner"
    PATH_GYM = "gym"
    PATH_DISCIPLINE = "discipline"
    PATH_TOURNAMENT = "tournament"
    PATH_75_HARD = "75_hard"

    PATH_CHOICES = [
        (PATH_RUNNER, "Runner"),
        (PATH_GYM, "Gym"),
        (PATH_DISCIPLINE, "Discipline"),
        (PATH_TOURNAMENT, "Tournament"),
        (PATH_75_HARD, "75 Hard"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="player",
    )

    level = models.PositiveIntegerField(default=1)
    exp = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)

    # Path selected by player. Used by quest assignment logic.
    path = models.CharField(max_length=20, choices=PATH_CHOICES, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Player({self.user.username})"
