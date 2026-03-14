from django.urls import path
from .views import QuestListView

urlpatterns = [
    path("", QuestListView.as_view(), name="quest-list"),
]