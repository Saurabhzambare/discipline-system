import math
import random
from dataclasses import dataclass
from datetime import date, timedelta

from django.db import transaction
from django.utils import timezone
from zoneinfo import ZoneInfo

from paths.models import (
    DisciplineCode,
    EquipmentProfile,
    PostFirstDollarChain,
    QuestChain,
    SingularGoal,
    SplitDayState,
    UserPathSelection,
    XPMultiplier,
)
from paths.mechanics import (
    FIRST_DOLLAR_CHAIN_100_PACK,
    FIRST_DOLLAR_CHAIN_10_PACK,
    FIRST_DOLLAR_CHAIN_MONTHLY_PACK,
    apply_missed_day_protections,
    apply_post_completion_mechanics,
)

from .models import (
    CrossPathBonus,
    DailyCompletionSummary,
    DailyIntention,
    DailyQuestLineup,
    DailyQuestLineupItem,
    DailySwap,
    PlayerDailyQuestAssignment,
    Quest,
    QuestCompletion,
    QuestFeedback,
    QuestPreference,
)


RANK_UNLOCK_BY_LEVEL = {
    1: {"D"},
    5: {"D", "C"},
    10: {"D", "C", "B"},
    20: {"D", "C", "B", "A"},
    30: {"D", "C", "B", "A", "S"},
}

STARTER_LINEUPS = {
    "fitness_warrior": [
        "Complete 20 Pushups",
        "Walk 5000 Steps",
        "Hit Your Protein Target",
    ],
    "mindset_sage": [
        "Meditate for 5 Minutes",
        "Write 3 Things You Are Grateful For",
        "Sit in Silence for 5 Minutes",
    ],
    "health_alchemist": [
        "Drink 2L of Water",
        "Alchemist Morning Protocol",
        "Eat One Whole Food Meal",
    ],
    "discipline_knight": [
        "Make Your Bed",
        "Write Tomorrow's Schedule",
        "Clean Your Workspace",
    ],
    "grind_visionary": [
        "30 Minutes on Your Grind Focus",
        "Singular Goal Check-In",
        "Log One Thing You Learned",
    ],
}

CROSS_PATH_BONUS_PAIRS = [
    ("cold_shower", {"fitness_warrior", "health_alchemist"}, 20),
    ("breathwork", {"mindset_sage", "health_alchemist"}, 20),
    ("deep_work", {"discipline_knight", "grind_visionary"}, 20),
    ("wake_5am", {"mindset_sage", "discipline_knight"}, 25),
    ("reading", {"mindset_sage", "grind_visionary"}, 25),
]

DIFFICULTY_MULTIPLIERS = {
    Quest.DIFFICULTY_EASY: 1.0,
    Quest.DIFFICULTY_MEDIUM: 1.3,
    Quest.DIFFICULTY_HARD: 1.6,
}


@dataclass
class LineupFeatures:
    days_on_path: int

    @property
    def slots_visible(self):
        return self.days_on_path >= 7

    @property
    def swaps_unlocked(self):
        return self.days_on_path >= 14

    @property
    def full_customization(self):
        return self.days_on_path >= 30


# ── shared helpers ────────────────────────────────────────────────────────────

def calculate_level_from_exp(exp: int) -> int:
    return max(1, int(math.sqrt((exp + 50) / 50)))


def calculate_exp_window(exp: int) -> dict:
    level = calculate_level_from_exp(exp)
    current_level_floor = (level**2 * 50) - 50
    next_level_floor = ((level + 1) ** 2 * 50) - 50
    exp_in_level = max(0, exp - current_level_floor)
    exp_to_next_level = max(0, next_level_floor - exp)
    return {
        "level": level,
        "current_level_floor": current_level_floor,
        "next_level_floor": next_level_floor,
        "exp_in_level": exp_in_level,
        "exp_for_level": max(1, next_level_floor - current_level_floor),
        "exp_to_next_level": exp_to_next_level,
    }


def calculate_scaled_exp(*, quest: Quest) -> int:
    multiplier = DIFFICULTY_MULTIPLIERS.get(quest.difficulty, 1.0)
    return max(1, int(round(quest.exp_reward * multiplier)))


def is_quest_scheduled_for_date(*, quest: Quest, date):
    if quest.recurrence == Quest.RECURRENCE_DAILY:
        return True
    if quest.recurrence == Quest.RECURRENCE_WEEKDAYS:
        return date.weekday() < 5
    if quest.recurrence == Quest.RECURRENCE_WEEKLY:
        return date.weekday() == 0
    return True


def _get_player_local_date(player, now=None):
    now = now or timezone.now()
    try:
        tz = ZoneInfo(player.timezone or "UTC")
    except Exception:  # noqa: BLE001
        tz = ZoneInfo("UTC")
    return now.astimezone(tz).date()


def _days_on_path(player, path_code: str, target_date: date) -> int:
    selection = UserPathSelection.objects.filter(player=player).first()
    if not selection or selection.path != path_code:
        return 1
    return max(1, (target_date - selection.committed_at.date()).days + 1)


def _allowed_ranks_for_level(level: int) -> set[str]:
    allowed = {"D"}
    for required_level, ranks in sorted(RANK_UNLOCK_BY_LEVEL.items()):
        if level >= required_level:
            allowed = ranks
    if "E" in allowed:
        allowed.remove("E")
    return allowed


def _eligible_path_queryset(player, path_code: str):
    return Quest.objects.filter(is_active=True, path_target=path_code)


def _recently_completed_quest_ids(player, lookback_days: int = 30):
    since = timezone.localdate() - timedelta(days=lookback_days)
    return set(
        QuestCompletion.objects.filter(player=player, completion_date__gte=since).values_list("quest_id", flat=True)
    )


def _within_cooldown(player, quest: Quest, target_date: date) -> bool:
    if quest.cooldown_days <= 0:
        return False
    last = (
        QuestCompletion.objects.filter(player=player, quest=quest)
        .order_by("-completion_date")
        .values_list("completion_date", flat=True)
        .first()
    )
    if not last:
        return False
    return (target_date - last).days <= quest.cooldown_days


def _equipment_ok(player, quest: Quest) -> bool:
    if not quest.equipment_required:
        return True
    equipment = EquipmentProfile.objects.filter(player=player).values_list("equipment_list", flat=True).first() or []
    return quest.equipment_required in equipment


def _serialize_item(item: DailyQuestLineupItem) -> dict:
    q = item.quest
    return {
        "item_id": item.id,
        "quest_id": q.id if q else None,
        "title": q.title if q else "Choose your own quest",
        "description": q.description if q else "",
        "path_target": q.path_target if q else item.lineup.path,
        "rank": q.rank if q else "",
        "pillar": q.pillar if q else "",
        "exp_reward": q.exp_reward if q else 0,
        "slot_order": item.slot_order,
        "slot_type": item.slot_type,
        "is_locked": item.is_locked,
        "is_carried_over": item.is_carried_over,
        "selection_reason": item.selection_reason,
        "completed_today": item.completed,
        "assigned_completed_today": item.completed,
        "feedback": item.feedback,
    }


def serialize_lineup(lineup: DailyQuestLineup) -> dict:
    items = list(lineup.items.select_related("quest", "swapped_from_quest").all())
    features = LineupFeatures(days_on_path=_days_on_path(lineup.player, lineup.path, lineup.date))
    return {
        "id": lineup.id,
        "path": lineup.path,
        "date": lineup.date.isoformat(),
        "intention": lineup.intention,
        "is_complete": lineup.is_complete,
        "days_on_path": features.days_on_path,
        "features_unlocked": {
            "slot_labels": features.slots_visible,
            "swap": features.swaps_unlocked,
            "full_customization": features.full_customization,
        },
        "swaps_remaining": max(0, 3 - DailySwap.objects.filter(player=lineup.player, path=lineup.path, swap_date=lineup.date).count()),
        "items": [_serialize_item(item) for item in items],
    }


# ── generation algorithm ───────────────────────────────────────────────────────

def _get_universal_quest(player, target_date: date, yesterday_lineup: DailyQuestLineup | None):
    pool = list(Quest.objects.filter(is_active=True, universal_daily=True).order_by("id"))
    if not pool:
        return None
    if not yesterday_lineup:
        return random.choice(pool)
    yesterday_universal = yesterday_lineup.items.filter(slot_type=DailyQuestLineupItem.SLOT_UNIVERSAL).values_list("quest_id", flat=True).first()
    candidates = [q for q in pool if q.id != yesterday_universal] or pool
    return random.choice(candidates)


def _get_hard_filtered_quests(player, path_code: str, target_date: date, limit: int = 3):
    allowed_ranks = _allowed_ranks_for_level(player.level)
    quests = []
    for quest in _eligible_path_queryset(player, path_code).filter(rank__in=allowed_ranks).order_by("id"):
        if quest.universal_daily:
            continue
        if _within_cooldown(player, quest, target_date):
            continue
        if path_code == "health_alchemist" and not _equipment_ok(player, quest):
            continue
        quests.append(quest)
    return quests[:limit]


def _apply_path_overrides(player, path_code: str, quests: list[Quest], target_date: date):
    if path_code == "fitness_warrior":
        split = SplitDayState.objects.filter(player=player).values_list("current_split", flat=True).first() or "push"
        if split == "rest":
            rest_candidates = [q for q in quests if q.is_rest_day_quest]
            if rest_candidates:
                return rest_candidates
        filtered = [q for q in quests if split in q.title.lower() or split in q.description.lower()]
        return filtered or quests

    if path_code == "health_alchemist":
        chain_edges = QuestChain.objects.select_related("parent_quest", "child_quest").filter(parent_quest__path_target=path_code)
        completed = set(QuestCompletion.objects.filter(player=player).values_list("quest_id", flat=True))
        for edge in chain_edges:
            if edge.parent_quest_id in completed and edge.child_quest_id not in completed:
                if edge.child_quest not in quests:
                    quests = [edge.child_quest] + quests
                break
        return quests

    if path_code == "discipline_knight" and target_date.weekday() == 6:
        sunday = Quest.objects.filter(path_target=path_code, title__icontains="honor review", is_active=True).first()
        if sunday and sunday not in quests:
            quests = [sunday] + quests
        return quests

    if path_code == "grind_visionary":
        if SingularGoal.objects.filter(player=player).exists():
            goal_quest = Quest.objects.filter(path_target=path_code, title__icontains="singular goal", is_active=True).first()
            if goal_quest and goal_quest not in quests:
                quests = [goal_quest] + quests
        chain = PostFirstDollarChain.objects.filter(player=player, chain_unlocked=True).first()
        if chain:
            next_pack = None
            if not chain.first_ten_completed:
                next_pack = FIRST_DOLLAR_CHAIN_10_PACK
            elif not chain.first_hundred_completed:
                next_pack = FIRST_DOLLAR_CHAIN_100_PACK
            elif not chain.first_monthly_completed:
                next_pack = FIRST_DOLLAR_CHAIN_MONTHLY_PACK
            if next_pack:
                chain_quest = Quest.objects.filter(path_target=path_code, pack_id=next_pack, is_active=True).first()
                if chain_quest and chain_quest not in quests:
                    quests = [chain_quest] + quests
        return quests

    if path_code == "mindset_sage":
        # V1 lightweight hook only; no Session 6 mechanics build-out here.
        _ = DisciplineCode.objects.filter(player=player).first()
        return quests

    return quests


def _apply_smart_suggestions(player, quests: list[Quest]):
    preferences = {
        pref.quest_id: pref.preference_score
        for pref in QuestPreference.objects.filter(player=player, quest_id__in=[q.id for q in quests])
    }
    recently_completed = _recently_completed_quest_ids(player)

    def score(quest):
        base = preferences.get(quest.id, 0)
        recency_penalty = -2 if quest.id in recently_completed else 0
        return base + recency_penalty

    return sorted(quests, key=score, reverse=True)


def _fill_fallback(player, path_code: str, selected_quests: list[Quest], target_date: date, needed: int):
    if needed <= 0:
        return selected_quests
    chosen_ids = {q.id for q in selected_quests}
    pool = []
    for q in _eligible_path_queryset(player, path_code).filter(rank__in=_allowed_ranks_for_level(player.level), is_active=True):
        if q.id in chosen_ids or q.universal_daily:
            continue
        if _within_cooldown(player, q, target_date):
            continue
        if path_code == "health_alchemist" and not _equipment_ok(player, q):
            continue
        pool.append(q)
    random.shuffle(pool)
    return selected_quests + pool[:needed]


def _get_carry_over_quests(player, path_code: str, target_date: date):
    yesterday = target_date - timedelta(days=1)
    prev_lineup = DailyQuestLineup.objects.filter(player=player, path=path_code, date=yesterday).first()
    if not prev_lineup:
        return []
    carry = []
    for item in prev_lineup.items.select_related("quest").filter(completed=False, quest__rank__in=["D", "C"]):
        if item.is_carried_over:
            continue
        carry.append(item.quest)
    return carry


def _check_cross_path_bonus(player, target_date: date, lineup_items: list[DailyQuestLineupItem]):
    selection = UserPathSelection.objects.filter(player=player).first()
    active_paths = set(selection.multi_paths_active if selection else ([] if not player.path else [player.path]))
    if len(active_paths) < 2:
        return None

    for key, pair_paths, bonus_exp in sorted(CROSS_PATH_BONUS_PAIRS, key=lambda x: x[2], reverse=True):
        if not pair_paths.issubset(active_paths):
            continue
        keywords = {
            "cold_shower": ["cold shower", "cold plunge"],
            "breathwork": ["breath", "meditate"],
            "deep_work": ["deep work"],
            "wake_5am": ["5am", "wake"],
            "reading": ["reading", "read"],
        }.get(key, [])
        matched = [
            item for item in lineup_items
            if item.quest and any(k in (item.quest.title + " " + item.quest.description).lower() for k in keywords)
        ]
        if len(matched) >= 2:
            return {"key": key, "bonus_exp": bonus_exp, "matched_item_ids": [i.id for i in matched[:2]]}
    return None


def _build_starter_quests(path_code: str):
    starter_titles = STARTER_LINEUPS.get(path_code, [])
    selected = []
    for phrase in starter_titles:
        q = Quest.objects.filter(path_target=path_code, title__icontains=phrase, rank="D", is_active=True).first()
        if q:
            selected.append(q)
    if len(selected) < 3:
        fillers = list(Quest.objects.filter(path_target=path_code, rank="D", is_active=True).exclude(id__in=[q.id for q in selected]).order_by("id")[:3-len(selected)])
        selected.extend(fillers)
    return selected[:3]


@transaction.atomic
def generate_daily_lineup(player, target_date: date | None = None, path_code: str | None = None, force: bool = False):
    target_date = target_date or _get_player_local_date(player)
    path_code = path_code or player.path
    if not path_code:
        raise ValueError("Player has no selected path.")

    existing = DailyQuestLineup.objects.filter(player=player, path=path_code, date=target_date).first()
    if existing and not force:
        return existing, False
    if existing and force:
        existing.delete()

    days_on_path = _days_on_path(player, path_code, target_date)
    yesterday_lineup = DailyQuestLineup.objects.filter(player=player, path=path_code, date=target_date - timedelta(days=1)).first()
    lineup = DailyQuestLineup.objects.create(player=player, path=path_code, date=target_date)

    slot_order = 1
    created_items = []
    universal = _get_universal_quest(player, target_date, yesterday_lineup)
    if universal:
        created_items.append(DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=universal,
            slot_order=slot_order,
            slot_type=DailyQuestLineupItem.SLOT_UNIVERSAL,
            is_locked=True,
            selection_reason=DailyQuestLineupItem.REASON_UNIVERSAL,
        ))
        slot_order += 1

    if days_on_path == 1:
        for q in _build_starter_quests(path_code):
            created_items.append(DailyQuestLineupItem.objects.create(
                lineup=lineup,
                quest=q,
                slot_order=slot_order,
                slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
                selection_reason=DailyQuestLineupItem.REASON_DAY1_STARTER,
            ))
            slot_order += 1
        return lineup, True

    selected = []
    for carry in _get_carry_over_quests(player, path_code, target_date):
        selected.append((carry, DailyQuestLineupItem.REASON_CARRY_OVER, True))

    hard = _get_hard_filtered_quests(player, path_code, target_date, limit=4)
    hard = _apply_path_overrides(player, path_code, hard, target_date)
    hard = _apply_smart_suggestions(player, hard)

    for q in hard:
        if q.id not in [x[0].id for x in selected]:
            selected.append((q, DailyQuestLineupItem.REASON_PATH_CORE, False))

    base_quests = [x[0] for x in selected]
    base_quests = _fill_fallback(player, path_code, base_quests, target_date, needed=max(0, 3 - len(base_quests)))
    selected_ids = {q.id for q, _, _ in selected}
    for q in base_quests:
        if q.id not in selected_ids:
            selected.append((q, DailyQuestLineupItem.REASON_FALLBACK, False))
            selected_ids.add(q.id)

    for q, reason, carried in selected[:4]:
        created_items.append(DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=q,
            slot_order=slot_order,
            slot_type=DailyQuestLineupItem.SLOT_ASSIGNED,
            selection_reason=reason,
            is_carried_over=carried,
        ))
        slot_order += 1

    if days_on_path >= 7:
        created_items.append(DailyQuestLineupItem.objects.create(
            lineup=lineup,
            quest=None,
            slot_order=slot_order,
            slot_type=DailyQuestLineupItem.SLOT_BONUS,
            is_locked=False,
            selection_reason=DailyQuestLineupItem.REASON_FALLBACK,
        ))

    _check_cross_path_bonus(player, target_date, created_items)
    return lineup, True


def get_daily_lineup(player, target_date: date | None = None):
    target_date = target_date or _get_player_local_date(player)
    apply_missed_day_protections(player=player, today=target_date)
    if not player.path:
        return {"lineup": None, "message": "No active path selected."}
    lineup = DailyQuestLineup.objects.filter(player=player, path=player.path, date=target_date).first()
    if not lineup:
        selection = UserPathSelection.objects.filter(player=player).first()
        if not selection or not selection.onboarding_complete:
            return {"lineup": None, "message": "Complete path onboarding to unlock daily quests."}
        if target_date != _get_player_local_date(player):
            return {"lineup": None, "message": "No lineup exists for that date."}
        lineup, _ = generate_daily_lineup(player=player, target_date=target_date, path_code=player.path)
    return {"lineup": serialize_lineup(lineup)}


# ── completion / feedback / swaps / intention ─────────────────────────────────

def _count_completed(lineup: DailyQuestLineup):
    qs = lineup.items.all()
    completed = qs.filter(completed=True).count()
    total = qs.exclude(slot_type=DailyQuestLineupItem.SLOT_BONUS).count()
    return completed, total


@transaction.atomic
def detect_cross_path_bonus(player, target_date: date):
    if CrossPathBonus.objects.filter(player=player, bonus_date=target_date).exists():
        return 0
    items = DailyQuestLineupItem.objects.filter(
        lineup__player=player,
        lineup__date=target_date,
        completed=True,
        quest__isnull=False,
    ).select_related("quest", "lineup")

    selection = UserPathSelection.objects.filter(player=player).first()
    active_paths = set(selection.multi_paths_active if selection else ([player.path] if player.path else []))
    if len(active_paths) < 2:
        return 0

    completed_by_path = {}
    for item in items:
        completed_by_path.setdefault(item.lineup.path, []).append(item.quest)

    keyword_map = {
        "cold_shower": ["cold shower", "cold plunge"],
        "breathwork": ["breath", "meditate"],
        "deep_work": ["deep work"],
        "wake_5am": ["5am", "wake"],
        "reading": ["reading", "read"],
    }
    for key, pair_paths, bonus_exp in sorted(CROSS_PATH_BONUS_PAIRS, key=lambda x: x[2], reverse=True):
        if not pair_paths.issubset(active_paths):
            continue
        paths = list(pair_paths)
        p1, p2 = paths[0], paths[1]
        if p1 not in completed_by_path or p2 not in completed_by_path:
            continue
        def has_keyword(quests, keys):
            for q in quests:
                text = f"{q.title} {q.description}".lower()
                if any(k in text for k in keys):
                    return True
            return False
        keys = keyword_map.get(key, [])
        if has_keyword(completed_by_path[p1], keys) and has_keyword(completed_by_path[p2], keys):
            CrossPathBonus.objects.create(
                player=player,
                bonus_date=target_date,
                bonus_pair_key=key,
                pillars_completed=[p1, p2],
                bonus_exp=bonus_exp,
            )
            return bonus_exp
    return 0


@transaction.atomic
def generate_completion_summary(player, summary_date: date):
    lineup = DailyQuestLineup.objects.filter(player=player, path=player.path, date=summary_date).first()
    if not lineup:
        raise ValueError("No lineup for requested date.")

    completed, total = _count_completed(lineup)
    today_completions = QuestCompletion.objects.filter(player=player, completion_date=summary_date)
    base_exp = sum(today_completions.values_list("quest__exp_reward", flat=True))
    bonus_exp = CrossPathBonus.objects.filter(player=player, bonus_date=summary_date).values_list("bonus_exp", flat=True).first() or 0

    yesterday = summary_date - timedelta(days=1)
    streak_status = "maintained"
    if QuestCompletion.objects.filter(player=player, completion_date=yesterday).exists() and completed > 0:
        streak_status = "increased"
    elif completed == 0:
        streak_status = "at_risk"

    summary, _ = DailyCompletionSummary.objects.update_or_create(
        player=player,
        summary_date=summary_date,
        defaults={
            "lineup": lineup,
            "path": lineup.path,
            "quests_completed": completed,
            "quests_total": total,
            "total_exp_earned": base_exp + bonus_exp,
            "bonus_exp_earned": bonus_exp,
            "streak_status": streak_status,
            "streak_maintained": completed > 0,
            "cross_path_bonus_earned": bonus_exp > 0,
        },
    )
    return summary


@transaction.atomic
def complete_lineup_item(player, lineup_item_id: int):
    item = DailyQuestLineupItem.objects.select_for_update().select_related("lineup", "lineup__player").filter(
        id=lineup_item_id,
        lineup__player=player,
    ).first()
    if not item:
        raise ValueError("Lineup item not found.")
    local_today = _get_player_local_date(player)
    if item.lineup.date != local_today:
        raise ValueError("Only today's lineup items can be completed.")
    if item.completed:
        raise ValueError("Quest already completed.")
    if not item.quest:
        raise ValueError("Bonus slot has no selected quest.")

    now = timezone.now()
    item.completed = True
    item.completed_at = now
    item.save(update_fields=["completed", "completed_at"])

    QuestCompletion.objects.get_or_create(
        player=player,
        quest=item.quest,
        completion_date=local_today,
        defaults={"completed_at": now},
    )

    old_level = player.level
    exp_earned = item.quest.exp_reward
    if item.lineup.path == "grind_visionary":
        multiplier = XPMultiplier.objects.filter(player=player).values_list("multiplier", flat=True).first()
        if multiplier:
            exp_earned = int(round(exp_earned * float(multiplier)))

    bonus_exp = detect_cross_path_bonus(player, local_today)
    player.exp += exp_earned + bonus_exp
    player.level = calculate_level_from_exp(player.exp)

    if player.last_active_date:
        if (local_today - player.last_active_date).days == 1:
            player.streak += 1
        elif player.last_active_date != local_today:
            player.streak = 1
    else:
        player.streak = 1
    player.last_active_date = local_today
    player.save(update_fields=["exp", "level", "streak", "last_active_date", "updated_at"])

    mechanic_result = apply_post_completion_mechanics(
        player=player,
        lineup_path=item.lineup.path,
        completion_date=local_today,
        quest=item.quest,
    )
    if mechanic_result.bonus_exp:
        player.exp += mechanic_result.bonus_exp
        player.level = calculate_level_from_exp(player.exp)
        player.save(update_fields=["exp", "level", "updated_at"])

    completed, total = _count_completed(item.lineup)
    if completed >= total > 0:
        item.lineup.is_complete = True
        item.lineup.save(update_fields=["is_complete"])
        generate_completion_summary(player, local_today)

    return {
        "item_completed": True,
        "exp_earned": exp_earned,
        "bonus_exp": bonus_exp,
        "player_exp": player.exp,
        "player_level": player.level,
        "level_up": player.level > old_level,
        "new_level": player.level,
        "exp_progress": calculate_exp_window(player.exp),
        "streak_update": player.streak,
        "daily_progress": {"completed": completed, "total": total},
        "badges_earned": [],
        "mechanic_notes": mechanic_result.notes or [],
    }


def _swaps_allowed(player, lineup: DailyQuestLineup):
    features = LineupFeatures(days_on_path=_days_on_path(player, lineup.path, lineup.date))
    return features.swaps_unlocked or features.full_customization


def get_swap_alternatives(player, lineup_item_id: int):
    item = DailyQuestLineupItem.objects.select_related("lineup", "quest").filter(id=lineup_item_id, lineup__player=player).first()
    if not item:
        raise ValueError("Lineup item not found.")
    if item.slot_type in {DailyQuestLineupItem.SLOT_UNIVERSAL, DailyQuestLineupItem.SLOT_BONUS} or item.is_locked:
        raise ValueError("This slot cannot be swapped.")
    if not _swaps_allowed(player, item.lineup):
        raise ValueError("Swap unlocks on Day 14.")
    if not item.quest:
        raise ValueError("No quest assigned in this slot.")

    used_ids = set(item.lineup.items.values_list("quest_id", flat=True))
    rank_order = ["D", "C", "B", "A", "S"]
    idx = rank_order.index(item.quest.rank) if item.quest.rank in rank_order else 0
    allowed_ranks = {item.quest.rank}
    if idx > 0:
        allowed_ranks.add(rank_order[idx - 1])

    qs = Quest.objects.filter(is_active=True, path_target=item.lineup.path, rank__in=allowed_ranks).exclude(id__in=used_ids)
    candidates = []
    for q in qs:
        if _within_cooldown(player, q, item.lineup.date):
            continue
        if item.lineup.path == "health_alchemist" and not _equipment_ok(player, q):
            continue
        pref = QuestPreference.objects.filter(player=player, quest=q).values_list("preference_score", flat=True).first() or 0
        candidates.append((pref, q))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [q for _, q in candidates[:6]]


@transaction.atomic
def swap_quest(player, lineup_item_id: int, new_quest_id: int):
    item = DailyQuestLineupItem.objects.select_for_update().select_related("lineup", "quest").filter(id=lineup_item_id, lineup__player=player).first()
    if not item:
        raise ValueError("Lineup item not found.")
    alternatives = get_swap_alternatives(player, lineup_item_id)
    target = next((q for q in alternatives if q.id == new_quest_id), None)
    if not target:
        raise ValueError("Selected quest is not a valid alternative.")

    swaps_today = DailySwap.objects.filter(player=player, path=item.lineup.path, swap_date=item.lineup.date).count()
    if swaps_today >= 3:
        raise ValueError("Swap limit reached for today.")

    original = item.quest
    item.swapped_from_quest = original
    item.quest = target
    item.selection_reason = DailyQuestLineupItem.REASON_PATH_OVERRIDE
    item.save(update_fields=["swapped_from_quest", "quest", "selection_reason"])

    DailySwap.objects.create(
        player=player,
        path=item.lineup.path,
        swap_date=item.lineup.date,
        lineup_item=item,
        quest_removed=original,
        quest_added=target,
    )
    return serialize_lineup(item.lineup)


@transaction.atomic
def set_daily_intention(player, target_date: date, intention: str):
    if intention not in {"full_send", "steady", "recovery"}:
        raise ValueError("Invalid intention.")
    lineup = DailyQuestLineup.objects.filter(player=player, path=player.path, date=target_date).first()
    if not lineup:
        raise ValueError("No lineup exists for that date.")

    DailyIntention.objects.update_or_create(
        player=player,
        intention_date=target_date,
        defaults={"intention": intention},
    )
    lineup.intention = intention
    lineup.save(update_fields=["intention"])

    adjusted = False
    if intention == "steady":
        items = list(lineup.items.select_related("quest").filter(slot_type=DailyQuestLineupItem.SLOT_ASSIGNED, completed=False, quest__isnull=False))
        if items:
            hardest = max(items, key=lambda i: ["D", "C", "B", "A", "S"].index(i.quest.rank) if i.quest.rank in ["D", "C", "B", "A", "S"] else 0)
            easier_qs = Quest.objects.filter(path_target=lineup.path, rank__in=["D", "C"], is_active=True).exclude(id__in=lineup.items.values_list("quest_id", flat=True))
            replacement = easier_qs.first()
            if replacement:
                hardest.swapped_from_quest = hardest.quest
                hardest.quest = replacement
                hardest.selection_reason = DailyQuestLineupItem.REASON_INTENTION_ADJUSTMENT
                hardest.save(update_fields=["swapped_from_quest", "quest", "selection_reason"])
                adjusted = True

    elif intention == "recovery":
        incomplete_items = list(lineup.items.filter(slot_type=DailyQuestLineupItem.SLOT_ASSIGNED, completed=False).select_related("quest"))
        for item in incomplete_items:
            if item.quest and item.quest.rank != "D":
                replacement = Quest.objects.filter(path_target=lineup.path, rank="D", is_active=True).exclude(
                    id__in=lineup.items.values_list("quest_id", flat=True)
                ).first()
                if replacement:
                    item.swapped_from_quest = item.quest
                    item.quest = replacement
                    item.selection_reason = DailyQuestLineupItem.REASON_INTENTION_ADJUSTMENT
                    item.save(update_fields=["swapped_from_quest", "quest", "selection_reason"])
                    adjusted = True

    return {"intention_set": intention, "lineup_adjusted": adjusted}


@transaction.atomic
def submit_quest_feedback(player, lineup_item_id: int, feedback: str):
    if feedback not in {"up", "down"}:
        raise ValueError("Feedback must be 'up' or 'down'.")
    item = DailyQuestLineupItem.objects.select_related("lineup", "quest").filter(id=lineup_item_id, lineup__player=player).first()
    if not item or not item.quest:
        raise ValueError("Lineup item not found.")

    item.feedback = feedback
    item.save(update_fields=["feedback"])

    QuestFeedback.objects.update_or_create(
        player=player,
        quest=item.quest,
        defaults={"rating": feedback},
    )
    pref, _ = QuestPreference.objects.get_or_create(player=player, quest=item.quest)
    pref.preference_score = pref.preference_score + (1 if feedback == "up" else -1)
    if feedback == "up":
        pref.last_completed = item.lineup.date
    else:
        pref.last_skipped = item.lineup.date
    pref.save(update_fields=["preference_score", "last_completed", "last_skipped", "updated_at"])
    return {"saved": True, "feedback": feedback, "preference_score": pref.preference_score}


def check_missed_day(player):
    today = _get_player_local_date(player)
    if not player.last_active_date:
        return {"missed": False, "days_missed": 0}
    gap = (today - player.last_active_date).days
    return {"missed": gap > 1, "days_missed": max(0, gap - 1)}


# Backward compatibility wrappers used by existing UI/tests.
def assign_daily_quests(*, player, date=None):
    lineup, _ = generate_daily_lineup(player=player, target_date=date, path_code=player.path)
    for item in lineup.items.select_related("quest").all():
        if not item.quest:
            continue
        PlayerDailyQuestAssignment.objects.update_or_create(
            player=player,
            quest=item.quest,
            assignment_date=lineup.date,
            defaults={
                "assigned_exp_reward": calculate_scaled_exp(quest=item.quest),
                "completed": item.completed,
                "completed_at": item.completed_at,
            },
        )
    return PlayerDailyQuestAssignment.objects.filter(player=player, assignment_date=lineup.date).select_related("quest").order_by("quest_id")


def complete_quest(*, player, quest):
    today = _get_player_local_date(player)
    item = DailyQuestLineupItem.objects.filter(lineup__player=player, lineup__date=today, lineup__path=player.path, quest=quest).first()
    if not item:
        raise ValueError("Quest is not assigned for today.")
    try:
        result = complete_lineup_item(player, item.id)
    except ValueError as exc:
        if "already completed" in str(exc).lower():
            raise ValueError("Quest already completed today.") from exc
        raise
    return {
        "exp_gained": result["exp_earned"] + result["bonus_exp"],
        "player_exp": player.exp,
        "player_streak": player.streak,
        "old_level": max(1, result["new_level"] - (1 if result["level_up"] else 0)),
        "new_level": result["new_level"],
        "leveled_up": result["level_up"],
    }
