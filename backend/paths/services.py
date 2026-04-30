from datetime import timedelta

from django.db import transaction
from django.db.models import Count, Sum
from django.utils import timezone

from players.models import Player
from quests.models import QuestCompletion
from .models import (
    ArmorPiece,
    ArmorSystem,
    BodyJournal,
    DarkNightEntry,
    DisciplineCode,
    DisciplineKnightProfile,
    ElixirProgress,
    EquipmentProfile,
    FitnessWarriorProfile,
    GraceToken,
    GrindVisionaryProfile,
    HealthAlchemistProfile,
    KnightWeeklyReport,
    MultiplierProtection,
    MindsetSageProfile,
    PostFirstDollarChain,
    PathDiscoveryQuiz,
    PathMatchScore,
    PathOnboardingProgress,
    QuizAnswer,
    SingularGoal,
    SkillTree,
    SkillTreeNode,
    SplitDayState,
    StreakShield,
    TemptationLog,
    TransmutationMilestone,
    UserPathSelection,
    WarRoomEntry,
    WisdomLog,
    OutputLog,
    XPMultiplier,
)
from .quiz_data import PATH_CODES, calculate_path_scores, get_randomized_questions
from .constants import (
    MASTERY_LAB_PACK_IDS,
    SKILL_TREE_NODE_ORDER,
    SKILL_TREE_THRESHOLDS,
)

RETAKE_COOLDOWN_DAYS = 7
DISCIPLINE_BLOCKLIST = {
    "hate",
    "kill",
    "racist",
    "nazi",
    "terrorist",
    "slur",
}

GOAL_TIMELINE_DAYS = {
    "3_months": 90,
    "6_months": 180,
    "1_year": 365,
    "2_years": 730,
}

GV_SKILL_TREE_NODES = [
    "foundation",
    "consistency",
    "execution",
    "shipping",
    "audience",
    "monetization",
    "scaling",
]

PATH_NAMES = {
    "fitness_warrior":   "Fitness Warrior",
    "mindset_sage":      "Mindset Sage",
    "health_alchemist":  "Health Alchemist",
    "discipline_knight": "Discipline Knight",
    "grind_visionary":   "Grind Visionary",
}

WAR_ROOM_MORNING_EXP = 35
WAR_ROOM_EVENING_EXP = 35
WAR_ROOM_SAME_DAY_BONUS_EXP = 20


def _calculate_level_from_exp(exp: int) -> int:
    import math

    return max(1, int(math.sqrt((exp + 50) / 50)))


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
            "onboarding_complete": False,
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


def _upsert_onboarding_progress(*, player: Player, path_code: str, step: str, answers: dict):
    PathOnboardingProgress.objects.update_or_create(
        player=player,
        path=path_code,
        defaults={
            "current_step": step,
            "answers_snapshot": answers,
            "is_completed": False,
            "completed_at": None,
        },
    )


def _complete_onboarding(*, player: Player, path_code: str):
    PathOnboardingProgress.objects.update_or_create(
        player=player,
        path=path_code,
        defaults={
            "current_step": "complete",
            "is_completed": True,
            "completed_at": timezone.now(),
        },
    )
    UserPathSelection.objects.filter(player=player).update(onboarding_complete=True)


def get_onboarding_status(player: Player) -> dict:
    selection = UserPathSelection.objects.filter(player=player).first()
    if not selection:
        return {
            "path_selected": False,
            "path_code": None,
            "onboarding_complete": False,
            "current_step": None,
            "answers_snapshot": {},
        }
    progress = PathOnboardingProgress.objects.filter(
        player=player,
        path=selection.path,
    ).first()
    return {
        "path_selected": True,
        "path_code": selection.path,
        "onboarding_complete": selection.onboarding_complete,
        "current_step": progress.current_step if progress else "start",
        "answers_snapshot": progress.answers_snapshot if progress else {},
    }


@transaction.atomic
def save_fitness_warrior_onboarding(player: Player, payload: dict) -> dict:
    split = payload["training_split"]
    split_start = payload.get("split_day_start") or ""
    if split in {"ppl", "bro_split"} and not split_start:
        raise ValueError("split_day_start is required for PPL or Bro Split.")

    FitnessWarriorProfile.objects.update_or_create(
        player=player,
        defaults={
            "training_split": split,
            "primary_goal": payload["primary_goal"],
            "training_days_per_week": payload["training_days_per_week"],
            "experience_level": payload["experience_level"],
            "split_day_start": split_start,
        },
    )

    split_map = {"fresh_start": "push"}
    current_split = split_map.get(split_start, split_start or "push")
    SplitDayState.objects.update_or_create(
        player=player,
        defaults={"current_split": current_split, "last_updated": timezone.localdate()},
    )
    _upsert_onboarding_progress(
        player=player,
        path_code="fitness_warrior",
        step="fitness_profile_saved",
        answers=payload,
    )
    return {"saved": True, "path_code": "fitness_warrior", "current_step": "fitness_profile_saved"}


@transaction.atomic
def save_mindset_sage_onboarding(player: Player, payload: dict) -> dict:
    MindsetSageProfile.objects.update_or_create(
        player=player,
        defaults=payload,
    )
    _upsert_onboarding_progress(
        player=player,
        path_code="mindset_sage",
        step="mindset_profile_saved",
        answers=payload,
    )
    return {"saved": True, "path_code": "mindset_sage", "current_step": "mindset_profile_saved"}


@transaction.atomic
def save_health_alchemist_onboarding(player: Player, payload: dict) -> dict:
    HealthAlchemistProfile.objects.update_or_create(
        player=player,
        defaults={
            "primary_health_goal": payload["primary_health_goal"],
            "health_relationship": payload["health_relationship"],
            "focus_area": payload["focus_area"],
        },
    )
    EquipmentProfile.objects.update_or_create(
        player=player,
        defaults={"equipment_list": payload["equipment_list"]},
    )
    _upsert_onboarding_progress(
        player=player,
        path_code="health_alchemist",
        step="health_profile_saved",
        answers=payload,
    )
    return {"saved": True, "path_code": "health_alchemist", "current_step": "health_profile_saved"}


def get_alchemist_setup_guide(player: Player) -> dict:
    profile = HealthAlchemistProfile.objects.filter(player=player).first()
    if not profile:
        raise ValueError("Health Alchemist onboarding is incomplete.")

    disclaimer = (
        "These are general wellness suggestions not medical advice. "
        "Consult a healthcare professional before starting any new supplement protocol."
    )

    starter_pack = (
        "You do not need everything at once. Start with one change. "
        "Master it. Then add the next."
    )
    if profile.primary_health_goal == "reduce_stress_and_burnout":
        starter_pack = (
            "Your Starter Formula Alchemist: prioritize magnesium (or chamomile tea), "
            "cold shower recovery, and sleep tracking. "
            "You do not need everything at once. Start with one change. "
            "Master it. Then add the next."
        )
    elif profile.primary_health_goal == "improve_gut_health":
        starter_pack = (
            "Your Starter Formula Alchemist: add probiotic foods daily, remove ultra-processed food "
            "for 3 days, and log digestion each evening. "
            "You do not need everything at once. Start with one change. "
            "Master it. Then add the next."
        )

    return {
        "disclaimer_top": disclaimer,
        "disclaimer_bottom": disclaimer,
        "supplements": [
            {
                "key": "creatine",
                "name": "Creatine Monohydrate",
                "take_it": "Energy, strength, and cognitive support.",
                "eat_it_instead": "Red meat and fish.",
                "disclaimer": disclaimer,
            },
            {
                "key": "vitamin_d3",
                "name": "Vitamin D3",
                "take_it": "Immune, mood, and bone support.",
                "eat_it_instead": "Sunlight, fatty fish, egg yolks.",
                "disclaimer": disclaimer,
            },
            {
                "key": "omega3",
                "name": "Omega-3 Fish Oil",
                "take_it": "Inflammation reduction and brain health.",
                "eat_it_instead": "Salmon, sardines, walnuts, flaxseeds.",
                "disclaimer": disclaimer,
            },
        ],
        "equipment_cards": [
            {"key": "cold_plunge", "name": "Cold Plunge Setup", "budget_alternative": "Large storage bin + ice."},
            {"key": "sauna", "name": "Sauna Access", "budget_alternative": "Local gym/YMCA sauna."},
            {"key": "tracker", "name": "Fitness Tracker", "budget_alternative": "Mi Band/Fitbit-level devices."},
            {"key": "journal", "name": "Journal or Notebook", "budget_alternative": "Built-in app journal."},
        ],
        "starter_pack": {
            "goal": profile.primary_health_goal,
            "health_relationship": profile.health_relationship,
            "message": starter_pack,
        },
    }


@transaction.atomic
def save_discipline_knight_onboarding(player: Player, payload: dict) -> dict:
    DisciplineKnightProfile.objects.update_or_create(
        player=player,
        defaults=payload,
    )
    _upsert_onboarding_progress(
        player=player,
        path_code="discipline_knight",
        step="knight_profile_saved",
        answers=payload,
    )
    return {"saved": True, "path_code": "discipline_knight", "current_step": "knight_profile_saved"}


@transaction.atomic
def submit_discipline_code(player: Player, rules: list[str]) -> dict:
    normalized = [rule.strip() for rule in rules if rule and rule.strip()]
    if len(normalized) < 3 or len(normalized) > 5:
        raise ValueError("Discipline Code must include 3 to 5 rules.")

    blocked = []
    for rule in normalized:
        words = {w.strip(".,!?").lower() for w in rule.split()}
        if words & DISCIPLINE_BLOCKLIST:
            blocked.append(rule)
    if blocked:
        raise ValueError(
            "Your code contains content that violates community guidelines. "
            "Please rewrite it Knight."
        )

    DisciplineCode.objects.update_or_create(
        player=player,
        defaults={"code_items": normalized},
    )
    _upsert_onboarding_progress(
        player=player,
        path_code="discipline_knight",
        step="discipline_code_saved",
        answers={"rules": normalized},
    )
    return {"saved": True, "rules_count": len(normalized), "current_step": "discipline_code_saved"}


@transaction.atomic
def save_grind_visionary_onboarding(player: Player, payload: dict) -> dict:
    if payload["grind_focus"] != "other":
        payload["grind_focus_other"] = ""
    elif not payload.get("grind_focus_other", "").strip():
        raise ValueError("grind_focus_other is required when grind_focus is other.")

    GrindVisionaryProfile.objects.update_or_create(
        player=player,
        defaults={
            "grind_focus": payload["grind_focus"],
            "grind_focus_other": payload.get("grind_focus_other", "").strip(),
            "experience_state": payload["experience_state"],
            "daily_hours": payload["daily_hours"],
            "current_output_state": payload["current_output_state"],
        },
    )

    target_date = timezone.localdate() + timedelta(days=GOAL_TIMELINE_DAYS[payload["goal_timeline"]])
    SingularGoal.objects.update_or_create(
        player=player,
        defaults={
            "title": payload["singular_goal_text"].strip(),
            "description": f"Timeline: {payload['goal_timeline']}",
            "target_date": target_date,
            "is_achieved": False,
            "achieved_at": None,
        },
    )

    tree, _ = SkillTree.objects.get_or_create(player=player, path="grind_visionary")
    for index, node_key in enumerate(GV_SKILL_TREE_NODES):
        SkillTreeNode.objects.update_or_create(
            tree=tree,
            node_key=node_key,
            defaults={
                "is_unlocked": index == 0,
                "unlocked_at": timezone.now() if index == 0 else None,
            },
        )

    _upsert_onboarding_progress(
        player=player,
        path_code="grind_visionary",
        step="visionary_profile_saved",
        answers=payload,
    )
    return {"saved": True, "path_code": "grind_visionary", "current_step": "visionary_profile_saved"}


@transaction.atomic
def complete_path_onboarding(player: Player, path_code: str) -> dict:
    if path_code not in PATH_CODES:
        raise ValueError(f"Invalid path: {path_code}")
    _complete_onboarding(player=player, path_code=path_code)
    return {"completed": True, "path_code": path_code}


def count_mastery_lab_completions(*, player: Player) -> int:
    """Cumulative count of Mastery Lab quest completions for a player."""
    return QuestCompletion.objects.filter(
        player=player,
        quest__pack_id__in=MASTERY_LAB_PACK_IDS,
    ).count()


@transaction.atomic
def check_and_unlock_skill_tree_nodes(*, player: Player) -> list[str]:
    """
    Check Mastery Lab completions against SKILL_TREE_THRESHOLDS and unlock
    any newly-eligible skill tree nodes for the Grind Visionary path.
    Returns the list of node_keys that were just unlocked (so the frontend
    can celebrate them).
    """
    tree = SkillTree.objects.filter(player=player, path="grind_visionary").first()
    if not tree:
        return []

    completions = count_mastery_lab_completions(player=player)
    newly_unlocked: list[str] = []

    existing_nodes = {n.node_key: n for n in tree.nodes.all()}

    for node_key in SKILL_TREE_NODE_ORDER:
        threshold = SKILL_TREE_THRESHOLDS.get(node_key, 0)
        node = existing_nodes.get(node_key)
        if node is None:
            # Tree wasn't fully initialized — defer to onboarding to populate.
            continue
        if node.is_unlocked:
            continue
        if completions >= threshold:
            node.is_unlocked = True
            node.unlocked_at = timezone.now()
            node.save(update_fields=["is_unlocked", "unlocked_at"])
            newly_unlocked.append(node_key)

    return newly_unlocked


def list_wisdom_logs(*, player: Player):
    return WisdomLog.objects.filter(player=player).order_by("-log_date", "-id")


@transaction.atomic
def upsert_wisdom_log(*, player: Player, payload: dict):
    log_date = payload.get("log_date") or timezone.localdate()
    obj, _ = WisdomLog.objects.update_or_create(
        player=player,
        log_date=log_date,
        defaults={
            "entry": payload["entry"],
            "is_public": payload.get("is_public", False),
        },
    )
    return obj


@transaction.atomic
def create_dark_night(*, player: Player, payload: dict):
    from .mechanics import process_dark_night_entry

    entry_date = payload.get("date") or timezone.localdate()
    return process_dark_night_entry(player=player, entry=payload["entry"], entry_date=entry_date)


def list_body_journals(*, player: Player):
    return BodyJournal.objects.filter(player=player).order_by("-log_date", "-id")


@transaction.atomic
def upsert_body_journal(*, player: Player, payload: dict):
    log_date = payload.get("log_date") or timezone.localdate()
    defaults = {
        "weight_kg": payload.get("weight_kg"),
        "sleep_hours": payload.get("sleep_hours"),
        "energy_level": payload.get("energy_level"),
        "notes": payload.get("notes", ""),
        "is_public": False,
    }
    obj, _ = BodyJournal.objects.update_or_create(
        player=player,
        log_date=log_date,
        defaults=defaults,
    )
    return obj


def list_output_logs(*, player: Player):
    return OutputLog.objects.filter(player=player).order_by("-log_date", "-id")


@transaction.atomic
def upsert_output_log(*, player: Player, payload: dict):
    log_date = payload.get("log_date") or timezone.localdate()
    defaults = {
        "deep_work_hours": payload.get("deep_work_hours") or 0,
        "tasks_shipped": payload.get("tasks_shipped") or 0,
        "revenue_usd": payload.get("revenue_usd") or 0,
        "notes": payload.get("notes", ""),
        "is_public": payload.get("is_public", False),
    }
    obj, _ = OutputLog.objects.update_or_create(
        player=player,
        log_date=log_date,
        defaults=defaults,
    )
    return obj


def list_war_room_entries(*, player: Player):
    return WarRoomEntry.objects.filter(player=player).order_by("-week_start", "-id")


@transaction.atomic
def upsert_war_room_entry(*, player: Player, payload: dict):
    week_start = payload.get("week_start") or timezone.localdate()
    phase = payload["phase"]
    now = timezone.now()
    obj, _ = WarRoomEntry.objects.update_or_create(
        player=player,
        week_start=week_start,
        defaults={
            "objectives": payload.get("objectives", []),
            "reflection": payload.get("reflection", ""),
        },
    )
    exp_awarded = 0
    bonus_awarded = 0

    if phase == "morning":
        if payload.get("objectives"):
            obj.objectives = payload.get("objectives", [])
        if obj.morning_completed_at is None:
            obj.morning_completed_at = now
            obj.morning_exp_awarded = WAR_ROOM_MORNING_EXP
            exp_awarded += WAR_ROOM_MORNING_EXP

    if phase == "evening":
        if payload.get("reflection", "").strip():
            obj.reflection = payload.get("reflection", "")
        if obj.evening_completed_at is None:
            obj.evening_completed_at = now
            obj.evening_exp_awarded = WAR_ROOM_EVENING_EXP
            exp_awarded += WAR_ROOM_EVENING_EXP

    if obj.morning_completed_at and obj.evening_completed_at and not obj.same_day_bonus_awarded:
        obj.same_day_bonus_awarded = True
        obj.bonus_exp_awarded = WAR_ROOM_SAME_DAY_BONUS_EXP
        bonus_awarded = WAR_ROOM_SAME_DAY_BONUS_EXP

    obj.save(
        update_fields=[
            "objectives",
            "reflection",
            "morning_completed_at",
            "evening_completed_at",
            "morning_exp_awarded",
            "evening_exp_awarded",
            "bonus_exp_awarded",
            "same_day_bonus_awarded",
        ]
    )

    if exp_awarded or bonus_awarded:
        player.exp += exp_awarded + bonus_awarded
        player.level = _calculate_level_from_exp(player.exp)
        player.save(update_fields=["exp", "level", "updated_at"])

    obj._weekly_report_input = get_war_room_weekly_input(player=player, anchor_date=week_start)
    obj._exp_awarded = exp_awarded
    obj._bonus_awarded = bonus_awarded
    return obj


def get_war_room_weekly_input(*, player: Player, anchor_date):
    week_start = anchor_date - timedelta(days=anchor_date.weekday())
    week_end = week_start + timedelta(days=6)
    entries = WarRoomEntry.objects.filter(player=player, week_start__range=[week_start, week_end])
    mornings = entries.exclude(morning_completed_at__isnull=True).count()
    evenings = entries.exclude(evening_completed_at__isnull=True).count()
    bonuses = entries.filter(same_day_bonus_awarded=True).count()
    return {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "morning_plans_completed": mornings,
        "evening_reviews_completed": evenings,
        "same_day_bonuses": bonuses,
    }


@transaction.atomic
def generate_knight_weekly_report(*, player: Player, week_start):
    week_end = week_start + timedelta(days=6)
    war_room = get_war_room_weekly_input(player=player, anchor_date=week_start)
    armor = getattr(player, "armor_system", None)
    shield = getattr(player, "streak_shield", None)

    pillar_rows = (
        QuestCompletion.objects.filter(
            player=player,
            completion_date__range=[week_start, week_end],
            quest__path_target="discipline_knight",
        )
        .values("quest__pillar")
        .annotate(completions=Count("id"), exp_total=Sum("quest__exp_reward"))
        .order_by("quest__pillar")
    )
    pillar_performance = {
        row["quest__pillar"]: {
            "completions": row["completions"],
            "exp_total": row["exp_total"] or 0,
        }
        for row in pillar_rows
    }

    payload = {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "war_room": war_room,
        "armor": {
            "total_cracks": armor.total_cracks if armor else 0,
            "last_cracked_on": armor.last_cracked_on.isoformat() if armor and armor.last_cracked_on else None,
            "pieces_forged": player.armor_pieces.count(),
        },
        "streak": {
            "current_streak": player.streak,
            "shield_available": shield.shields_available if shield else 0,
            "shield_last_earned_date": shield.last_earned_date.isoformat() if shield and shield.last_earned_date else None,
        },
        "pillar_performance": pillar_performance,
    }

    report, _ = KnightWeeklyReport.objects.update_or_create(
        player=player,
        week_start=week_start,
        defaults={
            "week_end": week_end,
            "report_payload": payload,
        },
    )
    return report


def get_knight_weekly_report(*, player: Player, week_start):
    return KnightWeeklyReport.objects.filter(player=player, week_start=week_start).first()


def list_temptation_logs(*, player: Player):
    return TemptationLog.objects.filter(player=player).order_by("-log_date", "-id")


@transaction.atomic
def create_temptation_log(*, player: Player, payload: dict):
    log_date = payload.get("log_date") or timezone.localdate()
    return TemptationLog.objects.create(
        player=player,
        description=payload["description"].strip(),
        resisted=payload.get("resisted", True),
        log_date=log_date,
    )


def get_health_mechanics_status(*, player: Player):
    progress = ElixirProgress.objects.filter(player=player).first()
    milestones = list(
        TransmutationMilestone.objects.filter(player=player)
        .order_by("-achieved_on", "-id")
        .values("milestone_key", "achieved_on")[:10]
    )
    return {
        "elixir": {
            "elixir_level": progress.elixir_level if progress else 1,
            "current_formula": progress.current_formula if progress else "",
            "brews_completed": progress.brews_completed if progress else 0,
            "fill_days": progress.fill_days if progress else 0,
            "mercy_retained_fill_days": progress.mercy_retained_fill_days if progress else 0,
            "last_brew_date": progress.last_brew_date if progress else None,
            "last_fill_date": progress.last_fill_date if progress else None,
        },
        "transmutation_milestones": milestones,
    }


def get_discipline_mechanics_status(*, player: Player):
    armor = ArmorSystem.objects.filter(player=player).first()
    shield = StreakShield.objects.filter(player=player).first()
    grace_available = GraceToken.objects.filter(player=player, is_used=False).count()
    pieces = list(
        ArmorPiece.objects.filter(player=player).values("slot", "name", "is_equipped", "earned_at")
    )
    return {
        "armor": {
            "total_cracks": armor.total_cracks if armor else 0,
            "last_cracked_on": armor.last_cracked_on if armor else None,
            "repaired_at": armor.repaired_at if armor else None,
            "pieces": pieces,
        },
        "grace_tokens": {"available": grace_available},
        "streak_shield": {
            "shields_available": shield.shields_available if shield else 0,
            "last_earned_date": shield.last_earned_date if shield else None,
        },
    }


def get_grind_mechanics_status(*, player: Player):
    multiplier = XPMultiplier.objects.filter(player=player).first()
    protections = MultiplierProtection.objects.filter(player=player, is_used=False).count()
    tree = SkillTree.objects.filter(player=player, path="grind_visionary").first()
    chain = PostFirstDollarChain.objects.filter(player=player).first()
    unlocked_nodes = tree.nodes.filter(is_unlocked=True).count() if tree else 0
    total_nodes = tree.nodes.count() if tree else 0
    return {
        "xp_multiplier": {
            "multiplier": float(multiplier.multiplier) if multiplier else 1.0,
            "source": multiplier.source if multiplier else "",
            "expires_at": multiplier.expires_at if multiplier else None,
        },
        "multiplier_protection": {
            "available": protections,
        },
        "skill_tree": {
            "exists": bool(tree),
            "unlocked_nodes": unlocked_nodes,
            "total_nodes": total_nodes,
        },
        "first_dollar_chain": {
            "first_dollar_completed": chain.first_dollar_completed if chain else False,
            "chain_unlocked": chain.chain_unlocked if chain else False,
            "chain_stage": chain.chain_stage if chain else 0,
            "current_chain": chain.current_chain if chain else 0,
            "longest_chain": chain.longest_chain if chain else 0,
        },
    }
