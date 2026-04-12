from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quest
from .serializers import (
    AdaptiveDifficultyDecisionSerializer,
    CompleteLineupItemSerializer,
    DailyIntentionSerializer,
    DailyLineupQuerySerializer,
    DailySummaryQuerySerializer,
    QuestCompleteSerializer,
    QuestFeedbackSerializer,
    QuestSerializer,
    SwapAlternativeQuestSerializer,
    SwapAlternativesQuerySerializer,
    SwapQuestSerializer,
)
from .services import (
    check_missed_day,
    complete_lineup_item,
    complete_quest,
    generate_completion_summary,
    get_daily_lineup,
    get_swap_alternatives,
    serialize_lineup,
    get_completion_ring_data,
    get_end_of_day_summary_payload,
    get_tomorrow_preview,
    get_adaptive_difficulty_nudge,
    set_adaptive_difficulty_decision,
    set_daily_intention,
    submit_quest_feedback,
    swap_quest,
)


class QuestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = DailyLineupQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        target_date = serializer.validated_data.get("date")
        payload = get_daily_lineup(request.user.player, target_date=target_date)
        lineup = payload.get("lineup")
        if lineup is None:
            return Response(payload, status=status.HTTP_200_OK)
        quests = [
            {
                "quest_id": item["quest_id"],
                "title": item["title"],
                "description": item["description"],
                "path_target": item["path_target"],
                "rank": item["rank"],
                "pillar": item["pillar"],
                "exp_reward": item["exp_reward"],
                "completed_today": item["completed_today"],
                "assigned_completed_today": item["assigned_completed_today"],
                "universal_daily": item["slot_type"] == "universal",
                "is_weekly_boss": item["selection_reason"] == "weekly_rhythm",
                "cooldown_days": 0,
            }
            for item in lineup["items"]
            if item["quest_id"]
        ]
        return Response(QuestSerializer(quests, many=True).data)


class QuestCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quest_id = serializer.validated_data["quest_id"]
        try:
            quest = Quest.objects.get(id=quest_id, is_active=True)
        except Quest.DoesNotExist:
            return Response({"detail": "Quest not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = complete_quest(player=request.user.player, quest=quest)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Quest completed successfully.", **result}, status=status.HTTP_200_OK)


class DailyLineupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = DailyLineupQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        target_date = serializer.validated_data.get("date")
        payload = get_daily_lineup(request.user.player, target_date=target_date)
        if payload.get("lineup") is None:
            return Response(payload)
        payload["missed_day"] = check_missed_day(request.user.player)
        return Response(payload)


class DailyLineupCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompleteLineupItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = complete_lineup_item(request.user.player, serializer.validated_data["item_id"])
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class SwapAlternativesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = SwapAlternativesQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        try:
            alternatives = get_swap_alternatives(request.user.player, serializer.validated_data["item_id"])
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"alternatives": SwapAlternativeQuestSerializer(alternatives, many=True).data})


class AlternativesAliasView(SwapAlternativesView):
    """Backward-compatible alias for docs/older clients."""


class SwapQuestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SwapQuestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            updated = swap_quest(
                request.user.player,
                serializer.validated_data["item_id"],
                serializer.validated_data["new_quest_id"],
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"lineup": updated})


class DailyIntentionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DailyIntentionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = set_daily_intention(
                request.user.player,
                serializer.validated_data["date"],
                serializer.validated_data["intention"],
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class QuestFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = submit_quest_feedback(
                request.user.player,
                serializer.validated_data["item_id"],
                serializer.validated_data["feedback"],
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class DailySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = DailySummaryQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        target_date = serializer.validated_data.get("date") or timezone.localdate()
        try:
            payload = get_end_of_day_summary_payload(request.user.player, target_date)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(payload)


class DailySummaryTodayView(DailySummaryView):
    """Backward-compatible endpoint alias at /summary/today/."""


class CompletionRingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = DailySummaryQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        target_date = serializer.validated_data.get("date")
        return Response(get_completion_ring_data(request.user.player, target_date))


class TomorrowPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = DailySummaryQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        target_date = serializer.validated_data.get("date")
        return Response(get_tomorrow_preview(request.user.player, target_date))


class AdaptiveDifficultyNudgeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = DailySummaryQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        target_date = serializer.validated_data.get("date")
        return Response(get_adaptive_difficulty_nudge(request.user.player, target_date))

    def post(self, request):
        serializer = AdaptiveDifficultyDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(set_adaptive_difficulty_decision(request.user.player, serializer.validated_data["decision"]))
