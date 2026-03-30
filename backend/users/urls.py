from django.urls import path

from .views import GoogleAuthView, SignupView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="auth-signup"),
    path("google/", GoogleAuthView.as_view(), name="auth-google"),
]
