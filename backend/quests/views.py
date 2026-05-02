from django.db import models
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


# ── Weekly Boss ──────────────────────────────────────────────────────────────

class WeeklyBossView(APIView):
    """GET /api/quests/weekly-boss/ — current week's boss(es) for the player."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        import datetime as _dt

        from paths.models import UserPathSelection
        from social.models import Badge, UserBadge, WeeklyBossCompletion, WeeklyBossQuest

        player = request.user.player
        today = timezone.localdate()
        week_start = today - _dt.timedelta(days=today.weekday())
        week_end = week_start + _dt.timedelta(days=6)

        # Determine player's active paths.
        active_paths = {player.path}
        selection = UserPathSelection.objects.filter(player=player).first()
        if selection and selection.multi_paths_active:
            active_paths.update(selection.multi_paths_active)

        # Fetch bosses for active paths in the current week.
        bosses_qs = WeeklyBossQuest.objects.filter(
            week_start=week_start,
            is_active=True,
        ).filter(
            # path_target="" means all-path boss, or specific path in active set.
            models.Q(path_target="") | models.Q(path_target__in=active_paths),
        )

        # Pre-fetch completions for this player + these bosses.
        boss_ids = [b.id for b in bosses_qs]
        completions_map = {}
        for comp in WeeklyBossCompletion.objects.filter(player=player, boss_id__in=boss_ids):
            completions_map[comp.boss_id] = comp

        # Pre-fetch badge info for completed bosses that have a badge awarded.
        earned_badge_keys = set(
            UserBadge.objects.filter(player=player).values_list("badge__key", flat=True)
        )

        result_bosses = []
        for boss in bosses_qs:
            comp = completions_map.get(boss.id)
            completion_data = None
            state = "available"
            if comp:
                state = "completed"
                # Determine badge awarded text.
                badge_awarded = None
                if boss.badge and boss.badge.key in earned_badge_keys:
                    badge_awarded = boss.badge.key
                completion_data = {
                    "id": comp.id,
                    "completed_at": comp.completed_at.isoformat() if comp.completed_at else None,
                    "exp_awarded": comp.exp_awarded,
                    "badge_awarded": badge_awarded,
                }
            result_bosses.append({
                "id": boss.id,
                "path": boss.path_target,
                "title": boss.title,
                "description": boss.description,
                "exp_reward": boss.exp_reward,
                "requirements": None,
                "completion": completion_data,
                "state": state,
            })

        return Response({
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "bosses": result_bosses,
        })


class CompleteWeeklyBossView(APIView):
    """POST /api/quests/weekly-boss/complete/ — defeat a weekly boss."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        from social.achievements import complete_weekly_boss

        boss_id = request.data.get("boss_id")
        if boss_id is None:
            return Response(
                {"detail": "boss_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            boss_id = int(boss_id)
        except (TypeError, ValueError):
            return Response(
                {"detail": "boss_id must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = complete_weekly_boss(request.user.player, boss_id)
        except ValueError as exc:
            error_msg = str(exc)
            # Map known validation errors to appropriate HTTP status codes.
            if "not available in the current week" in error_msg:
                return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)
            if "not active on" in error_msg:
                return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)
            if "not found" in error_msg:
                return Response({"detail": error_msg}, status=status.HTTP_404_NOT_FOUND)
            return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        if result.get("already_completed"):
            return Response(
                {"detail": "You have already defeated this boss this week."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response({
            "completion": {
                "id": result.get("achievement_card_id"),
                "completed_at": timezone.now().isoformat(),
                "exp_awarded": result["exp_awarded"],
            },
            "exp_awarded": result["exp_awarded"],
            "badge_awarded": result["badges_earned"][0] if result.get("badges_earned") else None,
            "badges_earned": result.get("badges_earned", []),
            "achievement_card_id": result.get("achievement_card_id"),
            "player_exp": result.get("player_exp"),
            "player_level": result.get("player_level"),
            "level_up": result.get("level_up", False),
        })

