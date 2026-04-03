from django.urls import path

from .views import (
    DailyIntentionView,
    DailyLineupCompleteView,
    DailyLineupView,
    DailySummaryView,
    QuestCompleteView,
    QuestFeedbackView,
    QuestListView,
    SwapAlternativesView,
    SwapQuestView,
)

urlpatterns = [
    path("", QuestListView.as_view(), name="quest-list"),
    path("complete/", QuestCompleteView.as_view(), name="quest-complete"),
    path("daily/", DailyLineupView.as_view(), name="quest-daily"),
    path("daily/complete/", DailyLineupCompleteView.as_view(), name="quest-daily-complete"),
    path("swap-alternatives/", SwapAlternativesView.as_view(), name="quest-swap-alternatives"),
    path("swap/", SwapQuestView.as_view(), name="quest-swap"),
    path("intention/", DailyIntentionView.as_view(), name="quest-intention"),
    path("feedback/", QuestFeedbackView.as_view(), name="quest-feedback"),
    path("summary/", DailySummaryView.as_view(), name="quest-summary"),
]
