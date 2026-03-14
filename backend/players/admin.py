from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Admin configuration for player records.
    This helps us inspect player progression data
    such as EXP, level, and streak.
    """

    list_display = ("id", "user", "level", "exp", "streak")
    search_fields = ("user__username",)