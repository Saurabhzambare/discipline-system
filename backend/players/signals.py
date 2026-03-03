"""
signals.py

This file contains Django signals.
Signals allow us to automatically run code
when certain events happen (like creating a new User).
"""

from django.conf import settings  # Allows safe reference to AUTH_USER_MODEL
from django.db.models.signals import post_save  # Signal triggered after a model is saved
from django.dispatch import receiver  # Decorator to connect a function to a signal

from .models import Player  # Import the Player model


# Connect this function to the "post_save" signal of the User model
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_player(sender, instance, created, **kwargs):
    """
    This function runs automatically AFTER a User is saved.

    Parameters explained:
    - sender: the model class that sent the signal (User model)
    - instance: the actual User object that was saved
    - created: Boolean (True if this was a new object creation)
    - **kwargs: extra arguments Django sends (we don't use them here)
    """

    # We ONLY want to create a Player when the User is FIRST created
    # Not every time the User is updated
    if created:
        Player.objects.create(user=instance)