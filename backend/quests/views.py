from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quest
from .serializers import QuestSerializer


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