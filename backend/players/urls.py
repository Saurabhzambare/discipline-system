"""
players/urls.py

This file defines URL routes specifically for the players app.
Each route maps a URL path to a view that handles the request.
"""

from django.urls import path        # Used to define URL patterns
from .views import PlayerMeView     # Import the API view that returns the logged-in player's profile


urlpatterns = [

    # Route: /api/player/me/
    #
    # When a GET request is sent to this URL,
    # Django will run the PlayerMeView.
    #
    # PlayerMeView.as_view() converts the class-based view
    # into a callable view function that Django can execute.
    #
    # name="player-me" gives this route a name so it can be
    # referenced elsewhere in Django (for reverse URL lookup).
    path("me/", PlayerMeView.as_view(), name="player-me"),
]