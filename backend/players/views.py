"""
views.py

This file defines API endpoints for the players app.
Here we create an endpoint that returns the logged-in player's profile.
"""

# Import permission class that allows only authenticated users
from rest_framework.permissions import IsAuthenticated

# Import Response class used to send JSON responses
from rest_framework.response import Response

# APIView is the base class for creating class-based API views in DRF
from rest_framework.views import APIView

# Import the serializer that converts Player objects into JSON
from .serializers import PlayerSerializer


class PlayerMeView(APIView):
    """
    API endpoint that returns the logged-in player's profile.

    URL example:
        GET /api/player/me/
    """

    # This ensures only authenticated users can access this endpoint.
    # If a request does not include a valid JWT token,
    # the API will return:
    #
    # 401 Unauthorized
    #
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests.

        request.user is automatically set by Django REST Framework
        after authentication is verified.
        """

        # Get the Player profile linked to the logged-in user
        player = request.user.player

        # Convert the Player object into JSON using the serializer
        serializer = PlayerSerializer(player)

        # Return the serialized data as an API response
        return Response(serializer.data)