from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quest
from .serializers import QuestSerializer, QuestCompleteSerializer
from .services import assign_daily_quests, complete_quest


class QuestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assignments = assign_daily_quests(player=request.user.player)
        serializer = QuestSerializer(assignments, many=True)
        return Response(serializer.data)


class QuestCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quest_id = serializer.validated_data["quest_id"]

        try:
            quest = Quest.objects.get(id=quest_id, is_active=True)
        except Quest.DoesNotExist:
            return Response(
                {"detail": "Quest not found or inactive."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            result = complete_quest(player=request.user.player, quest=quest)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Quest completed successfully.",
                **result,
            },
            status=status.HTTP_200_OK,
        )
