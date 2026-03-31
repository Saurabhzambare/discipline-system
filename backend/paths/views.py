from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from players.serializers import PlayerSerializer
from .serializers import CompleteQuizSerializer, SelectPathSerializer, SubmitAnswerSerializer
from .services import (
    complete_quiz,
    get_active_paths,
    retake_quiz,
    select_path,
    start_quiz,
    submit_answer,
)


class QuizStartView(APIView):
    """POST /api/paths/quiz/start/ — start or restart the identity quiz."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            result = start_quiz(player=request.user.player)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)


class QuizAnswerView(APIView):
    """POST /api/paths/quiz/answer/ — submit one answer."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data

        try:
            result = submit_answer(
                quiz_id=d["quiz_id"],
                question_number=d["question_number"],
                answer_key=d["answer"],
                player=request.user.player,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, **result})


class QuizCompleteView(APIView):
    """POST /api/paths/quiz/complete/ — score the quiz and return results."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompleteQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            results = complete_quiz(
                quiz_id=serializer.validated_data["quiz_id"],
                player=request.user.player,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"results": results})


class PathSelectView(APIView):
    """POST /api/paths/select/ — commit path selection after commitment screen."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SelectPathSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = select_path(
                player=request.user.player,
                path_code=serializer.validated_data["path_code"],
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # Re-fetch player so path field reflects the update
        request.user.player.refresh_from_db()
        player_data = PlayerSerializer(request.user.player).data

        return Response({**result, "player": player_data})


class ActivePathsView(APIView):
    """GET /api/paths/active/ — return player's active path(s)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = get_active_paths(player=request.user.player)
        return Response(result)


class QuizRetakeView(APIView):
    """POST /api/paths/retake/ — start a new quiz retake (7-day cooldown)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            result = retake_quiz(player=request.user.player)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)
