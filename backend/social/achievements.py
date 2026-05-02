"""Badge award, achievement card generation, and milestone check services."""

from django.db import transaction
from django.utils import timezone

from players.models import Player

from .models import AchievementCard, Badge, UserBadge, WeeklyBossCompletion, WeeklyBossQuest


# Exact path combinations required for each cross-path title badge.
_CROSS_PATH_TITLE_REQUIREMENTS: list[tuple[set[str], str]] = [
    # Order: most-specific first so all eligible titles are checked.
    (
        {"fitness_warrior", "mindset_sage", "health_alchemist", "discipline_knight", "grind_visionary"},
        "title_renaissance_human",
    ),
    (
        {"fitness_warrior", "mindset_sage", "health_alchemist", "discipline_knight"},
        "title_complete_human",
    ),
    (
        {"fitness_warrior", "mindset_sage", "health_alchemist"},
        "title_optimized_human",
    ),
    (
        {"fitness_warrior", "mindset_sage"},
        "title_warrior_sage",
    ),
]

_STREAK_MILESTONE_KEYS = {
    7: "streak_7",
    30: "streak_30",
    100: "streak_100",
    365: "streak_365",
}

_LEVEL_MILESTONE_KEYS = {
    5: "level_5",
    10: "level_10",
    20: "level_20",
    30: "level_30",
}


def award_badge(player: Player, badge_key: str, *, idempotent: bool = True) -> "UserBadge | None":
    """Award a badge by key. Returns None if already held and idempotent=True."""
    try:
        badge = Badge.objects.get(key=badge_key)
    except Badge.DoesNotExist:
        return None

    if idempotent:
        ub, created = UserBadge.objects.get_or_create(
            player=player,
            badge=badge,
        )
        return ub if created else None

    return UserBadge.objects.create(player=player, badge=badge)


def generate_achievement_card(
    player: Player,
    card_type: str,
    *,
    title: str,
    subtitle: str = "",
    metadata: dict | None = None,
) -> AchievementCard:
    return AchievementCard.objects.create(
        player=player,
        card_type=card_type,
        title=title,
        subtitle=subtitle,
        metadata=metadata or {},
    )



def grant_cross_path_title(player: Player) -> list[Badge]:
    """
    Check which cross-path titles the player qualifies for based on their
    exact active path combinations and award the appropriate badges.

    Returns list of newly-awarded Badge objects.

    Title requirements (per game design):
    - Warrior-Sage: fitness_warrior + mindset_sage
    - The Optimized Human: fitness_warrior + mindset_sage + health_alchemist
    - The Complete Human: above + discipline_knight
    - The Renaissance Human: all five paths

    V1: Active-path-combination only.
    TODO: Add 7-day consistency-window check in Session 9 verification.
    """
    from paths.models import UserPathSelection

    # Build the set of active path codes.
    active_paths: set[str] = set()

    selection = UserPathSelection.objects.filter(player=player).first()
    if selection and selection.multi_paths_active:
        active_paths.update(selection.multi_paths_active)

    # Fallback: include player.path if it's set.
    if player.path:
        active_paths.add(player.path)

    if len(active_paths) < 2:
        return []

    awarded: list[Badge] = []
    for required_paths, badge_key in _CROSS_PATH_TITLE_REQUIREMENTS:
        if required_paths.issubset(active_paths):
            ub = award_badge(player, badge_key)
            if ub:
                awarded.append(ub.badge)
    return awarded


def check_streak_milestones(player: Player) -> list[Badge]:
    """Check current streak against milestones and award any newly crossed badges."""
    awarded = []
    for threshold, key in _STREAK_MILESTONE_KEYS.items():
        if player.streak >= threshold:
            ub = award_badge(player, key)
            if ub:
                awarded.append(ub.badge)
    return awarded


def check_level_milestones(player: Player, old_level: int, new_level: int) -> list[Badge]:
    """Award level milestone badges for thresholds crossed in the old→new level range."""
    if new_level <= old_level:
        return []
    awarded = []
    for threshold, key in _LEVEL_MILESTONE_KEYS.items():
        if old_level < threshold <= new_level:
            ub = award_badge(player, key)
            if ub:
                awarded.append(ub.badge)
    return awarded


@transaction.atomic
def complete_weekly_boss(player: Player, boss_id: int) -> dict:
    """
    Record a player defeating a weekly boss and distribute rewards.

    Validations:
    - Boss must exist and be active.
    - Boss must belong to the current calendar week (Monday–Sunday UTC).
    - Boss path_target must match the player's primary or active paths.
    - Duplicate completion is idempotent (returns ``already_completed``).

    Awards:
    - Path-specific boss badge (first boss) and/or generic boss-count badges
    - AchievementCard of type "weekly_boss_<path>"
    - Bonus EXP (boss.exp_reward) with Visionary multiplier applied if applicable

    Returns a dict summarising what was awarded.

    Raises ``ValueError`` for validation failures.
    """
    import datetime as _dt

    from paths.models import UserPathSelection, XPMultiplier
    from quests.services import calculate_level_from_exp

    try:
        boss = WeeklyBossQuest.objects.select_for_update().get(id=boss_id, is_active=True)
    except WeeklyBossQuest.DoesNotExist:
        raise ValueError("Weekly boss not found or inactive.")

    # ── Current-week validation ───────────────────────────────────────────
    today = timezone.localdate()
    current_week_start = today - _dt.timedelta(days=today.weekday())  # Monday
    if boss.week_start != current_week_start:
        raise ValueError("This weekly boss is not available in the current week.")

    # ── Active-path validation ────────────────────────────────────────────
    if boss.path_target:
        active_paths = {player.path}
        selection = UserPathSelection.objects.filter(player=player).first()
        if selection and selection.multi_paths_active:
            active_paths.update(selection.multi_paths_active)
        if boss.path_target not in active_paths:
            raise ValueError("This weekly boss is for a path you are not active on.")

    completion, created = WeeklyBossCompletion.objects.get_or_create(
        player=player,
        boss=boss,
    )
    if not created:
        return {"already_completed": True}

    # Determine EXP reward with Visionary multiplier.
    base_exp = boss.exp_reward
    multiplier = 1.0
    if player.path == "grind_visionary":
        m = XPMultiplier.objects.filter(player=player).values_list("multiplier", flat=True).first()
        if m:
            multiplier = float(m)
    exp_awarded = int(round(base_exp * multiplier))

    completion.exp_awarded = exp_awarded
    completion.save(update_fields=["exp_awarded"])

    old_level = player.level
    player.exp += exp_awarded
    player.level = calculate_level_from_exp(player.exp)
    player.save(update_fields=["exp", "level", "updated_at"])

    badges_earned = []

    # Path-specific first-boss badge.
    path_boss_key_map = {
        "fitness_warrior": "fw_boss_week_1",
        "mindset_sage": "ms_boss_week_1",
        "health_alchemist": "ha_boss_week_1",
        "discipline_knight": "dk_boss_week_1",
        "grind_visionary": "gv_boss_week_1",
    }
    path_key = path_boss_key_map.get(boss.path_target or player.path)
    if path_key:
        ub = award_badge(player, path_key)
        if ub:
            badges_earned.append(ub.badge.key)

    # Universal boss count badges.
    total_boss_completions = WeeklyBossCompletion.objects.filter(player=player).count()
    for threshold, key in [(1, "boss_slayer_first"), (5, "boss_slayer_5"), (10, "boss_slayer_10")]:
        if total_boss_completions >= threshold:
            ub = award_badge(player, key)
            if ub:
                badges_earned.append(ub.badge.key)

    # Attach badge from boss definition if configured.
    if boss.badge:
        ub = award_badge(player, boss.badge.key)
        if ub:
            badges_earned.append(ub.badge.key)

    # Level milestone badges.
    level_badges = check_level_milestones(player, old_level, player.level)
    badges_earned.extend(b.key for b in level_badges)

    # Achievement card.
    path_label = (boss.path_target or player.path).replace("_", " ").title()
    card = generate_achievement_card(
        player,
        card_type=f"weekly_boss_{boss.path_target or player.path}",
        title=f"Boss Defeated: {boss.title}",
        subtitle=f"You defeated the {path_label} Weekly Boss for week of {boss.week_start}.",
        metadata={
            "boss_id": boss.id,
            "boss_title": boss.title,
            "exp_awarded": exp_awarded,
            "week_start": str(boss.week_start),
        },
    )

    return {
        "already_completed": False,
        "exp_awarded": exp_awarded,
        "player_exp": player.exp,
        "player_level": player.level,
        "level_up": player.level > old_level,
        "badges_earned": badges_earned,
        "achievement_card_id": card.id,
    }
