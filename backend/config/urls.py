"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


"""
urls.py (main project URL configuration)

This file defines the root URL routes for the entire Django project.
It tells Django which app should handle specific URL paths.
"""
from django.contrib import admin
from django.urls import path, include
from core.views import health



"""
Import JWT authentication views from the SimpleJWT package.

These views provide built-in endpoints for login and token refresh.
They save us from writing authentication logic manually.
"""
# TokenObtainPairView
# -------------------
# Handles user login.
# When a user sends their username and password,
# this view verifies the credentials and returns two tokens:
#
# 1. Access Token  → used to authenticate API requests
# 2. Refresh Token → used to generate a new access token when it expires
from rest_framework_simplejwt.views import TokenObtainPairView
# TokenRefreshView
# ----------------
# Used when the access token expires.
# The frontend sends the refresh token,
# and this view returns a new access token.
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),

    # "api/player/" is the base URL for all player-related API endpoints.
    # Instead of defining all player routes here, we delegate them to the players app.
    
    path("api/player/", include("players.urls")),
    # Example:
    # If players/urls.py contains:
    # path("me/", PlayerMeView.as_view())
    #
    # Then the final endpoint becomes:
    # /api/player/me/
    
    # ---------------------------------------------------------
    # LOGIN ENDPOINT
    # ---------------------------------------------------------
    # URL: /api/auth/token/
    #
    # This endpoint is used for user login.
    #
    # The client sends:
    #    username + password
    #
    # If the credentials are correct,
    # Django returns TWO tokens:
    #
    # 1️⃣ Access Token  → used for authenticated API requests
    # 2️⃣ Refresh Token → used to generate a new access token
    #
    # Example request:
    #
    # POST /api/auth/token/
    # {
    #   "username": "saurabh",
    #   "password": "mypassword"
    # }
    #
    # Example response:
    #
    # {
    #   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
    #   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
    # }
    #
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),


    # ---------------------------------------------------------
    # TOKEN REFRESH ENDPOINT
    # ---------------------------------------------------------
    # URL: /api/auth/token/refresh/
    #
    # Access tokens expire after some time.
    #
    # Instead of forcing the user to log in again,
    # the frontend can send the refresh token here
    # to receive a new access token.
    #
    # Example request:
    #
    # POST /api/auth/token/refresh/
    # {
    #   "refresh": "your_refresh_token"
    # }
    #
    # Example response:
    #
    # {
    #   "access": "new_access_token"
    # }
    #
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    
    
    path("api/quests/", include("quests.urls")),

]