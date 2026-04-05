from datetime import timedelta

from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from players.serializers import PlayerSerializer
from .serializers import (
    BodyJournalSerializer,
    CompleteQuizSerializer,
    DarkNightSerializer,
    DisciplineCodeSerializer,
    DisciplineKnightOnboardingSerializer,
    FitnessWarriorOnboardingSerializer,
    FreedomDayRedeemSerializer,
    GrindVisionaryOnboardingSerializer,
    HealthAlchemistOnboardingSerializer,
    MindsetSageOnboardingSerializer,
    KnightWeeklyReportQuerySerializer,
    OnboardingCompleteSerializer,
    SelectPathSerializer,
    SubmitAnswerSerializer,
    OutputLogSerializer,
    WarRoomEntrySerializer,
    WisdomLogSerializer,
)
from .services import (
    complete_quiz,
    create_dark_night,
    complete_path_onboarding,
    get_alchemist_setup_guide,
    get_active_paths,
    list_body_journals,
    list_output_logs,
    list_war_room_entries,
    list_wisdom_logs,
    get_onboarding_status,
    generate_knight_weekly_report,
    get_knight_weekly_report,
    retake_quiz,
    save_discipline_knight_onboarding,
    save_fitness_warrior_onboarding,
    save_grind_visionary_onboarding,
    save_health_alchemist_onboarding,
    save_mindset_sage_onboarding,
    select_path,
    start_quiz,
    submit_discipline_code,
    submit_answer,
    upsert_body_journal,
    upsert_output_log,
    upsert_war_room_entry,
    upsert_wisdom_log,
    get_war_room_weekly_input,
)
from .mechanics import get_vision_board_summary, redeem_freedom_day_token


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


class OnboardingStatusView(APIView):
    """GET /api/paths/onboarding/status/ — resume-safe status payload."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_onboarding_status(player=request.user.player))


class FitnessWarriorOnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FitnessWarriorOnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = save_fitness_warrior_onboarding(
                request.user.player, serializer.validated_data
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class MindsetSageOnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MindsetSageOnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = save_mindset_sage_onboarding(request.user.player, serializer.validated_data)
        return Response(result)


class HealthAlchemistOnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HealthAlchemistOnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = save_health_alchemist_onboarding(request.user.player, serializer.validated_data)
        return Response(result)


class AlchemistSetupGuideView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            result = get_alchemist_setup_guide(request.user.player)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class DisciplineKnightOnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DisciplineKnightOnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = save_discipline_knight_onboarding(request.user.player, serializer.validated_data)
        return Response(result)


class DisciplineCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DisciplineCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = submit_discipline_code(
                request.user.player, serializer.validated_data["rules"]
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class GrindVisionaryOnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GrindVisionaryOnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = save_grind_visionary_onboarding(request.user.player, serializer.validated_data)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class OnboardingCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OnboardingCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = complete_path_onboarding(
                request.user.player, serializer.validated_data["path_code"]
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        request.user.player.refresh_from_db()
        player_data = PlayerSerializer(request.user.player).data
        return Response({**result, "player": player_data})


class FreedomDayRedeemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FreedomDayRedeemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        redeem_date = serializer.validated_data.get("date") or timezone.localdate()
        try:
            token = redeem_freedom_day_token(player=request.user.player, redeem_date=redeem_date)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"redeemed": True, "token_id": token.id, "used_on": token.used_on})


class WisdomLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(WisdomLogSerializer(list_wisdom_logs(player=request.user.player), many=True).data)

    def post(self, request):
        serializer = WisdomLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = upsert_wisdom_log(player=request.user.player, payload=serializer.validated_data)
        return Response(WisdomLogSerializer(obj).data)


class DarkNightView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DarkNightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = create_dark_night(player=request.user.player, payload=serializer.validated_data)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"id": obj.id, "activated_on": obj.activated_on, "exp_awarded": obj.exp_awarded})


class BodyJournalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(BodyJournalSerializer(list_body_journals(player=request.user.player), many=True).data)

    def post(self, request):
        serializer = BodyJournalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = upsert_body_journal(player=request.user.player, payload=serializer.validated_data)
        return Response(BodyJournalSerializer(obj).data)


class OutputLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(OutputLogSerializer(list_output_logs(player=request.user.player), many=True).data)

    def post(self, request):
        serializer = OutputLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = upsert_output_log(player=request.user.player, payload=serializer.validated_data)
        return Response(OutputLogSerializer(obj).data)


class WarRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = list_war_room_entries(player=request.user.player)
        payload = []
        for entry in entries:
            payload.append({
                "id": entry.id,
                "week_start": entry.week_start,
                "phase": "morning" if entry.morning_completed_at else "evening",
                "objectives": entry.objectives,
                "reflection": entry.reflection,
                "morning_exp_awarded": entry.morning_exp_awarded,
                "evening_exp_awarded": entry.evening_exp_awarded,
                "bonus_exp_awarded": entry.bonus_exp_awarded,
                "same_day_bonus_awarded": entry.same_day_bonus_awarded,
                "weekly_report_input": get_war_room_weekly_input(player=request.user.player, anchor_date=entry.week_start),
                "created_at": entry.created_at,
            })
        return Response(payload)

    def post(self, request):
        serializer = WarRoomEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = upsert_war_room_entry(player=request.user.player, payload=serializer.validated_data)
        return Response({
            "id": obj.id,
            "week_start": obj.week_start,
            "phase": serializer.validated_data["phase"],
            "objectives": obj.objectives,
            "reflection": obj.reflection,
            "morning_exp_awarded": obj.morning_exp_awarded,
            "evening_exp_awarded": obj.evening_exp_awarded,
            "bonus_exp_awarded": obj.bonus_exp_awarded,
            "same_day_bonus_awarded": obj.same_day_bonus_awarded,
            "weekly_report_input": getattr(obj, "_weekly_report_input", {}),
            "exp_awarded_now": getattr(obj, "_exp_awarded", 0),
            "bonus_awarded_now": getattr(obj, "_bonus_awarded", 0),
            "created_at": obj.created_at,
        })


class VisionBoardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_vision_board_summary(player=request.user.player, today=timezone.localdate()))


class KnightWeeklyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = KnightWeeklyReportQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        week_start = serializer.validated_data.get("week_start") or (timezone.localdate() - timedelta(days=timezone.localdate().weekday()))
        report = get_knight_weekly_report(player=request.user.player, week_start=week_start)
        if not report:
            report = generate_knight_weekly_report(player=request.user.player, week_start=week_start)
        return Response({
            "week_start": report.week_start,
            "week_end": report.week_end,
            "report_payload": report.report_payload,
            "generated_at": report.generated_at,
        })
