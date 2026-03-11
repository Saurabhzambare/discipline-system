"""
apps.py

This file defines configuration for the 'players' Django app.
It tells Django how the app should behave when the project starts.
"""

from django.apps import AppConfig  # Base class used to configure Django applications


class PlayersConfig(AppConfig):
    """
    App configuration class for the 'players' app.
    Django reads this class when the project starts.
    """

    # This sets the default type of primary key field
    # that Django will use when creating models in this app.
    #
    # BigAutoField = 64-bit auto-incrementing integer
    # Example:
    # id = models.BigAutoField(primary_key=True)
    #
    # This is recommended for modern applications because it
    # supports a very large number of records.
    default_auto_field = "django.db.models.BigAutoField"

    # The name of the Django app.
    # This must match the folder name of the app.
    name = "players"

    def ready(self):
        """
        This method runs when Django starts the application.

        We use it to import signals so that Django registers them.
        Without this, our signal handlers would never run.
        """

        # Import the signals module from this app.
        # This ensures the signal decorators (like @receiver)
        # are executed and registered with Django.
        from . import signals  # noqa