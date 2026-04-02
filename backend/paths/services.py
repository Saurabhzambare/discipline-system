from django.db import transaction
from django.utils import timezone

from players.models import Player
from .models import PathDiscoveryQuiz, PathMatchScore, QuizAnswer, UserPathSelection
from .quiz_data import PATH_CODES, calculate_path_scores, get_randomized_questions

RETAKE_COOLDOWN_DAYS = 7

PATH_NAMES = {
    "fitness_warrior":   "Fitness Warrior",
    "mindset_sage":      "Mindset Sage",
    "health_alchemist":  "Health Alchemist",
    "discipline_knight": "Discipline Knight",
    "grind_visionary":   "Grind Visionary",
}


def start_quiz(player: Player) -> dict:
    """
    Start a new PathDiscoveryQuiz for the player.
    - Any incomplete quiz is deleted and replaced with a fresh one.
    - retake_count = number of previously completed quizzes.
    Returns: { quiz_id, questions: [...] }
    """
    PathDiscoveryQuiz.objects.filter(player=player, completed=False).delete()

    retake_count = PathDiscoveryQuiz.objects.filter(
        player=player, completed=True
    ).count()

    quiz = PathDiscoveryQuiz.objects.create(
        player=player,
        retake_count=retake_count,
    )
    return {"quiz_id": quiz.id, "questions": get_randomized_questions(seed=quiz.id)}


def submit_answer(
    quiz_id: int, question_number: int, answer_key: str, player: Player
) -> dict:
    """
    Record one answer. Validates ownership, range (1–9), key (A–E), no duplicate.
    Returns: { answered: int, remaining: int }
    """
    try:
        quiz = PathDiscoveryQuiz.objects.get(id=quiz_id, player=player, completed=False)
    except PathDiscoveryQuiz.DoesNotExist:
        raise ValueError("Quiz not found or already completed.")

    if not 1 <= question_number <= 9:
        raise ValueError("question_number must be 1–9.")

    if answer_key not in ("A", "B", "C", "D", "E"):
        raise ValueError("answer_key must be A, B, C, D, or E.")

    QuizAnswer.objects.update_or_create(
        quiz=quiz,
        question_number=question_number,
        defaults={"answer_key": answer_key},
    )

    answered = QuizAnswer.objects.filter(quiz=quiz).count()
    return {"answered": answered, "remaining": 9 - answered}


@transaction.atomic
def complete_quiz(quiz_id: int, player: Player) -> list:
    """
    Score the quiz, persist PathMatchScore records, mark as completed.
    Returns: list of path results sorted by match_percentage descending.
    [{ path_code, path_name, raw_score, match_percentage, rank }]
    """
    try:
        quiz = PathDiscoveryQuiz.objects.select_for_update().get(
            id=quiz_id, player=player, completed=False
        )
    except PathDiscoveryQuiz.DoesNotExist:
        raise ValueError("Quiz not found or already completed.")

    answers_qs = QuizAnswer.objects.filter(quiz=quiz)
    if answers_qs.count() < 9:
        raise ValueError("All 9 questions must be answered before completing the quiz.")

    answers = {a.question_number: a.answer_key for a in answers_qs}
    scores = calculate_path_scores(answers)

    PathMatchScore.objects.filter(quiz=quiz).delete()
    PathMatchScore.objects.bulk_create([
        PathMatchScore(
            quiz=quiz,
            path=path,
            raw_score=data["raw_score"],
            match_percentage=data["match_percentage"],
        )
        for path, data in scores.items()
    ])

    quiz.completed = True
    quiz.completed_at = timezone.now()
    quiz.save(update_fields=["completed", "completed_at"])

    sorted_results = sorted(
        scores.items(), key=lambda x: x[1]["match_percentage"], reverse=True
    )
    return [
        {
            "path_code":        path,
            "path_name":        PATH_NAMES[path],
            "raw_score":        data["raw_score"],
            "match_percentage": data["match_percentage"],
            "rank":             rank + 1,
        }
        for rank, (path, data) in enumerate(sorted_results)
    ]


@transaction.atomic
def select_path(player: Player, path_code: str) -> dict:
    """
    Commit path selection: create/update UserPathSelection, update Player.path.
    Uses update_or_create so retakers can switch paths.
    Returns: { selected_path: { code, name } }
    """
    if path_code not in PATH_CODES:
        raise ValueError(f"Invalid path: {path_code}")

    UserPathSelection.objects.update_or_create(
        player=player,
        defaults={
            "path": path_code,
            "multi_paths_active": [path_code],
        },
    )
    # Direct update bypasses stale player instance after select_for_update
    Player.objects.filter(pk=player.pk).update(path=path_code)

    return {"selected_path": {"code": path_code, "name": PATH_NAMES[path_code]}}


def get_active_paths(player: Player) -> dict:
    """
    Return the player's current path selection state.
    Returns: { primary_path, multi_paths_active, next_unlock_in_days }
    """
    try:
        selection = UserPathSelection.objects.get(player=player)
    except UserPathSelection.DoesNotExist:
        return {
            "primary_path": None,
            "multi_paths_active": [],
            "next_unlock_in_days": None,
        }

    days_active = (timezone.now().date() - selection.committed_at.date()).days
    days_to_next = max(0, selection.multi_path_unlock_day - days_active)

    return {
        "primary_path":        selection.path,
        "multi_paths_active":  selection.multi_paths_active,
        "next_unlock_in_days": days_to_next,
    }


def retake_quiz(player: Player) -> dict:
    """
    Start a retake. Enforces 7-day cooldown since last completion.
    Previous quiz records are preserved (never deleted).
    Returns same structure as start_quiz.
    """
    last = (
        PathDiscoveryQuiz.objects.filter(player=player, completed=True)
        .order_by("-completed_at")
        .first()
    )
    if last and last.completed_at:
        days_since = (timezone.now() - last.completed_at).days
        if days_since < RETAKE_COOLDOWN_DAYS:
            remaining = RETAKE_COOLDOWN_DAYS - days_since
            raise ValueError(f"You can retake the quiz in {remaining} day(s).")

    return start_quiz(player)
