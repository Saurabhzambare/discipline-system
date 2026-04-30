"""
Leaderboard service functions for the social domain.

Five leaderboards are exposed:
1. Weekly EXP per path (top players in a path by EXP earned this UTC week)
2. Global cross-path EXP (combined weekly EXP across all active paths)
3. Armor (permanent — Discipline Knight pieces forged, all-time)
4. Multiplier streak (Grind Visionary current active streak in days)
5. Output Log monthly (Grind Visionary entries this calendar month)

Week boundary is Monday 00:00 UTC for v1 simplicity. A future iteration
may switch to per-player local week.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone as dt_timezone
from typing import Optional

from django.db.models import Count, F, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce

from players.models import Player


MAX_LIMIT = 100
DEFAULT_LIMIT = 10
FULL_ARMOR_PIECES = 6  # gold prestige threshold (per design: fully forged knight)


def _clamp_limit(limit: int | None) -> int:
    if limit is None:
        return DEFAULT_LIMIT
    try:
        limit_int = int(limit)
    except (TypeError, ValueError):
        return DEFAULT_LIMIT
    if limit_int < 1:
        return DEFAULT_LIMIT
    return min(limit_int, MAX_LIMIT)


def _start_of_week_utc(now: datetime | None = None) -> datetime:
    """Monday 00:00 UTC of the current week (UTC)."""
    now = now or datetime.now(dt_timezone.utc)
    # weekday(): Mon=0..Sun=6
    monday_date = (now - timedelta(days=now.weekday())).date()
    return datetime.combine(monday_date, time.min, tzinfo=dt_timezone.utc)


def _start_of_month_utc(now: datetime | None = None) -> date:
    now = now or datetime.now(dt_timezone.utc)
    return now.date().replace(day=1)


def _rank_rows(rows: list[dict], *, limit: int) -> list[dict]:
    """Assign 1-based rank, slice to limit, preserve stable ordering."""
    out = []
    for idx, row in enumerate(rows[:limit], start=1):
        out.append({"rank": idx, **row})
    return out


def _user_rank(rows: list[dict], requesting_player: Optional[Player]) -> Optional[int]:
    if requesting_player is None:
        return None
    for idx, row in enumerate(rows, start=1):
        if row.get("player_id") == requesting_player.id:
            return idx
    return None


# ── Weekly EXP per path ──────────────────────────────────────────────────────

def weekly_exp_leaderboard(
    path: str,
    *,
    limit: int = DEFAULT_LIMIT,
    requesting_player: Optional[Player] = None,
) -> dict:
    """Top players in `path` by EXP earned in the current UTC week."""
    from quests.models import QuestCompletion

    limit = _clamp_limit(limit)
    week_start = _start_of_week_utc().date()

    qs = (
        QuestCompletion.objects.filter(
            quest__path_target=path,
            completion_date__gte=week_start,
        )
        .values("player_id", username=F("player__user__username"))
        # Use completion records so today's completions appear immediately,
        # without waiting for end-of-day summary generation.
        .annotate(exp=Coalesce(Sum("quest__exp_reward"), Value(0), output_field=IntegerField()))
        .filter(exp__gt=0)
        .order_by("-exp", "player_id")
    )
    rows = [
        {"player_id": r["player_id"], "username": r["username"], "exp": int(r["exp"])}
        for r in qs
    ]
    return {
        "leaderboard": _rank_rows(rows, limit=limit),
        "user_rank": _user_rank(rows, requesting_player),
    }


# ── Global cross-path weekly EXP ─────────────────────────────────────────────

def global_cross_path_leaderboard(
    *,
    limit: int = DEFAULT_LIMIT,
    requesting_player: Optional[Player] = None,
) -> dict:
    """Top players globally by total weekly EXP across all active paths.

    Uses raw quest-completion EXP (``quest.exp_reward``) from completion records.
    This intentionally avoids double-applying Visionary multipliers at read time.
    """
    from quests.models import QuestCompletion

    limit = _clamp_limit(limit)
    week_start = _start_of_week_utc().date()

    qs = (
        QuestCompletion.objects.filter(completion_date__gte=week_start)
        .values("player_id", username=F("player__user__username"))
        .annotate(exp=Coalesce(Sum("quest__exp_reward"), Value(0), output_field=IntegerField()))
        .filter(exp__gt=0)
        .order_by("-exp", "player_id")
    )
    rows = [
        {"player_id": r["player_id"], "username": r["username"], "exp": int(r["exp"])}
        for r in qs
    ]
    return {
        "leaderboard": _rank_rows(rows, limit=limit),
        "user_rank": _user_rank(rows, requesting_player),
    }


# ── Armor leaderboard (Discipline Knight, permanent) ─────────────────────────

def armor_leaderboard(
    *,
    limit: int = DEFAULT_LIMIT,
    requesting_player: Optional[Player] = None,
) -> dict:
    """Permanent leaderboard of Discipline Knight players by armor pieces forged."""
    from paths.models import ArmorPiece

    limit = _clamp_limit(limit)

    qs = (
        ArmorPiece.objects.filter(player__path=Player.PATH_DISCIPLINE_KNIGHT)
        .values("player_id", username=F("player__user__username"))
        .annotate(pieces=Count("id"))
        .filter(pieces__gt=0)
        .order_by("-pieces", "player_id")
    )
    rows = []
    for r in qs:
        pieces = int(r["pieces"])
        tier = "gold_prestige" if pieces >= FULL_ARMOR_PIECES else "silver"
        rows.append({
            "player_id": r["player_id"],
            "username": r["username"],
            "pieces": pieces,
            "tier": tier,
        })
    return {
        "leaderboard": _rank_rows(rows, limit=limit),
        "user_rank": _user_rank(rows, requesting_player),
    }


# ── Multiplier streak (Grind Visionary) ──────────────────────────────────────

def multiplier_streak_leaderboard(
    *,
    limit: int = DEFAULT_LIMIT,
    requesting_player: Optional[Player] = None,
) -> dict:
    """Top Grind Visionary players by current active multiplier streak in days."""
    from paths.models import XPMultiplier

    limit = _clamp_limit(limit)

    multiplier_qs = (
        XPMultiplier.objects
        .filter(
            player__path=Player.PATH_GRIND_VISIONARY,
            multiplier__gt=1.0,
        )
        .select_related("player__user")
    )
    rows = [
        {
            "player_id": m.player_id,
            "username": m.player.user.username,
            "streak_days": int(m.player.streak),
            "multiplier": float(m.multiplier),
        }
        for m in multiplier_qs
        if m.player.streak > 0
    ]
    rows.sort(key=lambda r: (-r["streak_days"], r["player_id"]))

    return {
        "leaderboard": _rank_rows(rows, limit=limit),
        "user_rank": _user_rank(rows, requesting_player),
    }


# ── Output Log monthly (Grind Visionary) ─────────────────────────────────────

def output_log_monthly_leaderboard(
    *,
    limit: int = DEFAULT_LIMIT,
    requesting_player: Optional[Player] = None,
) -> dict:
    """Top Grind Visionary players by Output Log entries in the current calendar month."""
    from paths.models import OutputLog

    limit = _clamp_limit(limit)
    month_start = _start_of_month_utc()

    qs = (
        OutputLog.objects.filter(
            player__path=Player.PATH_GRIND_VISIONARY,
            log_date__gte=month_start,
        )
        .values("player_id", username=F("player__user__username"))
        .annotate(output_count=Count("id"))
        .filter(output_count__gt=0)
        .order_by("-output_count", "player_id")
    )
    rows = [
        {
            "player_id": r["player_id"],
            "username": r["username"],
            "output_count": int(r["output_count"]),
        }
        for r in qs
    ]
    return {
        "leaderboard": _rank_rows(rows, limit=limit),
        "user_rank": _user_rank(rows, requesting_player),
    }
