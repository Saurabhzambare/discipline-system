"""
models.py

This file defines the Player model, which represents the
game profile attached to each user in the Discipline System.
"""

# Import project settings so we can reference the custom User model safely
from django.conf import settings

# Import Django's base model classes and field types
from django.db import models


class Player(models.Model):
    """
    Player model = the "game profile" for a user.

    In the Discipline System:
        User   → authentication identity (login)
        Player → game stats (level, EXP, streak)
    """

    # ---------------------------------------------------------
    # RELATIONSHIP TO USER
    # ---------------------------------------------------------
    # One-to-one relationship with the User model.
    #
    # This means:
    # - Each User has exactly ONE Player profile.
    # - Each Player belongs to exactly ONE User.
    #
    # settings.AUTH_USER_MODEL references the custom user model
    # defined in settings.py (users.User).
    #
    # on_delete=models.CASCADE means:
    # If the User is deleted, the Player is deleted automatically.
    #
    # related_name="player" allows us to access the player from
    # the user like this:
    #
    #     user.player
    #
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="player",
    )

    # ---------------------------------------------------------
    # GAME PROGRESSION FIELDS
    # ---------------------------------------------------------

    # Player's current level.
    # PositiveIntegerField ensures the value cannot be negative.
    # Default level is 1 when a new player is created.
    level = models.PositiveIntegerField(default=1)

    # Player's experience points.
    # This increases when quests are completed.
    exp = models.PositiveIntegerField(default=0)

    # Player's current streak (consecutive days completing tasks).
    # Example:
    # If a user completes tasks daily for 5 days → streak = 5
    streak = models.PositiveIntegerField(default=0)

    # ---------------------------------------------------------
    # TIMESTAMP FIELDS
    # ---------------------------------------------------------

    # Automatically set when the Player record is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically updated every time the Player record is saved.
    updated_at = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------
    # This controls how the object appears in:
    # - Django Admin
    # - Django shell
    #
    # Instead of:
    #   Player object (1)
    #
    # It will display:
    #   Player(saurabh)
    #
    def __str__(self):
        """
        Human-friendly display name for this object.
        Shows up in Django Admin and Django shell.

        Instead of: "Player object (1)"
        You'll see:  "Player(saurabh)"
        """
        return f"Player({self.user.username})"