"""
models.py

This file defines your Django database models.
A "model" = a Python class that Django converts into a database table.
"""

from django.conf import settings  # Lets us reference AUTH_USER_MODEL safely (custom User model)
from django.db import models      # Django's base tools for creating database tables (models)


class Player(models.Model):
    """
    Player = the "game profile" for a user in your Solo Leveling discipline system.

    Why separate Player from User?
    - User handles authentication (login, password, email, etc.)
    - Player handles game stats (level, exp, streak, etc.)

    This keeps your system clean and scalable.
    """

    # One-to-one relationship:
    # - Each User has exactly ONE Player
    # - Each Player belongs to exactly ONE User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Points to your custom User model (recommended best practice)
        on_delete=models.CASCADE,  # If the User is deleted, delete the Player too (prevents orphan data)
        related_name="player",     # Allows: user.player instead of user.player_set
    )

    # Core game stats ---------------------------------------------

    # Player's current level in the system (starts at 1)
    # PositiveIntegerField prevents negative numbers.
    level = models.PositiveIntegerField(default=1)

    # Player's experience points (EXP). Starts at 0.
    # Later: you'll add logic like "if exp >= 100 => level up"
    exp = models.PositiveIntegerField(default=0)

    # Consecutive days of completing quests/habits. Starts at 0.
    streak = models.PositiveIntegerField(default=0)

    # Timestamps ---------------------------------------------

    # Automatically set once when the Player is created.
    # Example: created_at = March 3, 2026 10:15 AM
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically updates every time you save/update the Player.
    # Example: updated_at changes when level/exp/streak changes.
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Human-friendly display name for this object.
        Shows up in Django Admin and Django shell.

        Instead of: "Player object (1)"
        You'll see:  "Player(saurabh)"
        """
        return f"Player({self.user.username})"