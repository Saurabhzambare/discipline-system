from django.urls import path

from .views import (
    AdaptiveDifficultyNudgeView,
    AlternativesAliasView,
    CompletionRingView,
    DailyIntentionView,
    DailyLineupCompleteView,
    DailyLineupView,
    DailySummaryView,
    DailySummaryTodayView,
    TomorrowPreviewView,
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
    path("alternatives/", AlternativesAliasView.as_view(), name="quest-alternatives-alias"),
    path("swap/", SwapQuestView.as_view(), name="quest-swap"),
    path("intention/", DailyIntentionView.as_view(), name="quest-intention"),
    path("feedback/", QuestFeedbackView.as_view(), name="quest-feedback"),
    path("summary/", DailySummaryView.as_view(), name="quest-summary"),
    path("summary/today/", DailySummaryTodayView.as_view(), name="quest-summary-today"),
    path("completion-ring/", CompletionRingView.as_view(), name="quest-completion-ring"),
    path("tomorrow-preview/", TomorrowPreviewView.as_view(), name="quest-tomorrow-preview"),
    path("adaptive-nudge/", AdaptiveDifficultyNudgeView.as_view(), name="quest-adaptive-nudge"),
]
