from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quest
from .serializers import QuestSerializer, QuestCompleteSerializer
from .services import complete_quest


class QuestListView(APIView):
    """
    API endpoint that returns all active quests.

    Example:
    GET /api/quests/

    Only authenticated users should be able to see quests.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests for listing quests.
        """

        # Fetch only active quests from the database
        quests = Quest.objects.filter(is_active=True)

        # Convert queryset into JSON using the serializer
        serializer = QuestSerializer(quests, many=True)

        # Return serialized data as API response
        return Response(serializer.data)


class QuestCompleteView(APIView):
    """
    API endpoint that lets an authenticated player complete a quest.

    Example:
    POST /api/quests/complete/
    {
        "quest_id": 1
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle quest completion requests.
        """

        # Validate incoming request data
        serializer = QuestCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract quest_id after validation succeeds
        quest_id = serializer.validated_data["quest_id"]

        try:
            # Only allow completing active quests
            quest = Quest.objects.get(id=quest_id, is_active=True)
        except Quest.DoesNotExist:
            return Response(
                {"detail": "Quest not found or inactive."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get the logged-in user's player profile
        player = request.user.player

        try:
            # Run the gameplay logic from the service layer
            result = complete_quest(player=player, quest=quest)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return success response with updated player progress
        return Response(
            {
                "message": "Quest completed successfully.",
                **result,
            },
            status=status.HTTP_200_OK,
        )