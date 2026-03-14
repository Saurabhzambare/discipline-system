from django.contrib import admin
from .models import Quest, QuestCompletion


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    """
    Admin configuration for reusable quest templates.
    This makes quests easier to view, search, and manage
    from the Django admin panel.
    """

    # Columns shown in the quest list page inside admin
    list_display = ("id", "title", "exp_reward", "is_active", "created_at")

    # Right-side filter options in admin
    list_filter = ("is_active",)

    # Search box support
    search_fields = ("title",)
    
@admin.register(QuestCompletion)
class QuestCompletionAdmin(admin.ModelAdmin):
    """
    Admin configuration for quest completion records.
    This helps us inspect which player completed which quest
    and when it happened.
    """

    # Columns shown in the completion list page inside admin
    list_display = ("id", "player", "quest", "completion_date", "completed_at")

    # Filter sidebar options
    list_filter = ("completion_date", "quest")

    # Search support by username and quest title
    search_fields = ("player__user__username", "quest__title")