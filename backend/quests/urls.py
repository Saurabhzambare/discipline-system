from django.urls import path
from .views import QuestListView, QuestCompleteView

urlpatterns = [
    # GET /api/quests/
    path("", QuestListView.as_view(), name="quest-list"),

    # POST /api/quests/complete/
    path("complete/", QuestCompleteView.as_view(), name="quest-complete"),
]