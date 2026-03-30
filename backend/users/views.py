import re

from django.conf import settings
from django.contrib.auth import get_user_model
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from players.models import Player

from .serializers import SignupSerializer

User = get_user_model()


def _unique_username(base):
    """Return a username derived from base that doesn't already exist."""
    # Strip characters that aren't allowed in usernames
    safe = re.sub(r'[^\w]', '', base) or 'hunter'
    username = safe
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{safe}{counter}"
        counter += 1
    return username


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "message": "Signup successful.",
            },
            status=status.HTTP_201_CREATED,
        )


class GoogleAuthView(APIView):
    """
    POST /api/auth/google/
    Body: { "credential": "<Google ID token>" }

    Verifies the Google ID token, finds or creates the matching user,
    ensures a Player profile exists, and returns JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        credential = request.data.get('credential', '').strip()
        if not credential:
            return Response({'detail': 'credential is required.'}, status=status.HTTP_400_BAD_REQUEST)

        client_id = settings.GOOGLE_CLIENT_ID
        if not client_id:
            return Response(
                {'detail': 'Google OAuth is not configured on this server.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Verify the ID token against Google's public certs
        try:
            idinfo = id_token.verify_oauth2_token(
                credential,
                google_requests.Request(),
                client_id,
            )
        except ValueError as exc:
            return Response(
                {'detail': f'Invalid Google token: {exc}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = idinfo.get('email')
        if not email:
            return Response(
                {'detail': 'Google account has no email address.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find or create the Django user by email
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': _unique_username(email.split('@')[0])},
        )

        # Ensure a Player profile exists
        Player.objects.get_or_create(user=user)

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'is_new': created,
        })
