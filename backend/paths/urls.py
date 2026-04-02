from django.urls import path

from .views import (
    ActivePathsView,
    PathSelectView,
    QuizAnswerView,
    QuizCompleteView,
    QuizRetakeView,
    QuizStartView,
)

urlpatterns = [
    path("quiz/start/",    QuizStartView.as_view(),    name="quiz-start"),
    path("quiz/answer/",   QuizAnswerView.as_view(),   name="quiz-answer"),
    path("quiz/complete/", QuizCompleteView.as_view(), name="quiz-complete"),
    path("select/",        PathSelectView.as_view(),   name="path-select"),
    path("active/",        ActivePathsView.as_view(),  name="path-active"),
    path("retake/",        QuizRetakeView.as_view(),   name="quiz-retake"),
]
