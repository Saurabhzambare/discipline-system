from django.urls import path

from .views import PlayerMeView, PlayerPathView

urlpatterns = [
    path("me/", PlayerMeView.as_view(), name="player-me"),
    path("path/", PlayerPathView.as_view(), name="player-path"),
]
