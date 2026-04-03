from django.urls import path

from .views import (
    AlchemistSetupGuideView,
    ActivePathsView,
    DisciplineCodeView,
    DisciplineKnightOnboardingView,
    FitnessWarriorOnboardingView,
    GrindVisionaryOnboardingView,
    HealthAlchemistOnboardingView,
    MindsetSageOnboardingView,
    OnboardingCompleteView,
    OnboardingStatusView,
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
    path("onboarding/status/", OnboardingStatusView.as_view(), name="onboarding-status"),
    path("onboarding/fitness-warrior/", FitnessWarriorOnboardingView.as_view(), name="onboarding-fitness-warrior"),
    path("onboarding/mindset-sage/", MindsetSageOnboardingView.as_view(), name="onboarding-mindset-sage"),
    path("onboarding/health-alchemist/", HealthAlchemistOnboardingView.as_view(), name="onboarding-health-alchemist"),
    path("onboarding/discipline-knight/", DisciplineKnightOnboardingView.as_view(), name="onboarding-discipline-knight"),
    path("onboarding/discipline-code/", DisciplineCodeView.as_view(), name="onboarding-discipline-code"),
    path("onboarding/grind-visionary/", GrindVisionaryOnboardingView.as_view(), name="onboarding-grind-visionary"),
    path("onboarding/health-alchemist/setup-guide/", AlchemistSetupGuideView.as_view(), name="alchemist-setup-guide"),
    path("onboarding/complete/", OnboardingCompleteView.as_view(), name="onboarding-complete"),
]
