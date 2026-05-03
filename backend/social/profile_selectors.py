"""Read-only assemblers for the public profile payload.

Builds path_profiles, badges, and achievement_cards summaries while enforcing
the privacy classification documented in C3D-1:

- Public-safe: high-level configuration, progression counts, multipliers,
  badge summaries, achievement card title/subtitle.
- Own-only: DisciplineCode.code_items, SingularGoal title/description,
  Mindset DarkNight counts.
- Do-not-expose: WisdomLog.entry, DarkNightEntry.entry, BodyJournal notes
  /weight/sleep/health details, OutputLog.notes.
"""

from __future__ import annotations

from django.db.models import Q

from paths.models import (
    PATH_CHOICES,
    ArmorPiece,
    ArmorSystem,
    BodyJournal,
    DarkNightEntry,
    DisciplineCode,
    ElixirProgress,
    FitnessWarriorProfile,
    FreedomDayToken,
    GraceToken,
    MindsetSageProfile,
    OutputLog,
    SingularGoal,
    SkillTree,
    SkillTreeNode,
    SplitDayState,
    StreakShield,
    TransmutationMilestone,
    UserPathSelection,
    WisdomLog,
    XPMultiplier,
)
from quests.models import QuestCompletion

# AccountabilityPartnership lives on the social app side.
from .models import AccountabilityPartnership, AchievementCard, UserBadge


PATH_LABELS = dict(PATH_CHOICES)

CROSS_PATH_TITLE_KEYS = {
    "title_warrior_sage",
    "title_optimized_human",
    "title_complete_human",
    "title_renaissance_human",
}


def active_paths_for(player):
    """Return ordered list of active path keys for this player."""
    selection = UserPathSelection.objects.filter(player=player).first()
    if selection and isinstance(selection.multi_paths_active, list) and selection.multi_paths_active:
        return [p for p in selection.multi_paths_active if p in PATH_LABELS]
    if player.path:
        return [player.path]
    return []


# ── PER-PATH SUMMARIES ───────────────────────────────────────────────────────


def _fitness_summary(player):
    profile = FitnessWarriorProfile.objects.filter(player=player).first()
    split_state = SplitDayState.objects.filter(player=player).first()
    completed = QuestCompletion.objects.filter(
        player=player, quest__path_target="fitness_warrior"
    ).count()
    return {
        "training_split": profile.training_split if profile else None,
        "primary_goal": profile.primary_goal if profile else None,
        "current_split": split_state.current_split if split_state else None,
        "completed_quests": completed,
    }


def _mindset_summary(player, *, is_own):
    profile = MindsetSageProfile.objects.filter(player=player).first()
    return {
        "archetype": profile.archetype if profile else None,
        "wisdom_log_count": WisdomLog.objects.filter(player=player).count(),
        "freedom_token_count": FreedomDayToken.objects.filter(player=player).count(),
        "dark_night_count": (
            DarkNightEntry.objects.filter(player=player).count() if is_own else None
        ),
    }


def _health_summary(player):
    elixir = ElixirProgress.objects.filter(player=player).first()
    latest_milestone = (
        TransmutationMilestone.objects.filter(player=player)
        .order_by("-achieved_on")
        .first()
    )
    return {
        "elixir_level": elixir.elixir_level if elixir else None,
        "brews_completed": elixir.brews_completed if elixir else 0,
        "fill_days": elixir.fill_days if elixir else 0,
        "mercy_retained_fill_days": elixir.mercy_retained_fill_days if elixir else 0,
        "body_journal_count": BodyJournal.objects.filter(player=player).count(),
        "transmutation_milestone_count": TransmutationMilestone.objects.filter(player=player).count(),
        "latest_transmutation": latest_milestone.milestone_key if latest_milestone else None,
    }


def _discipline_summary(player, *, is_own):
    armor_system = ArmorSystem.objects.filter(player=player).first()
    streak_shield = StreakShield.objects.filter(player=player).first()
    discipline_code = DisciplineCode.objects.filter(player=player).first()

    code_items = None
    if is_own and discipline_code and isinstance(discipline_code.code_items, list):
        code_items = list(discipline_code.code_items)

    return {
        "armor_piece_count": ArmorPiece.objects.filter(player=player).count(),
        "total_cracks": armor_system.total_cracks if armor_system else 0,
        "grace_token_count": GraceToken.objects.filter(player=player, is_used=False).count(),
        "streak_shields_available": streak_shield.shields_available if streak_shield else 0,
        "discipline_code": code_items,
    }


def _grind_summary(player, *, is_own):
    multiplier = XPMultiplier.objects.filter(player=player).first()
    singular_goal = SingularGoal.objects.filter(player=player).first()

    skill_tree = SkillTree.objects.filter(player=player, path="grind_visionary").first()
    if skill_tree:
        node_qs = SkillTreeNode.objects.filter(tree=skill_tree)
        unlocked_qs = node_qs.filter(is_unlocked=True)
        unlocked_count = unlocked_qs.count()
        total_count = node_qs.count()
        latest_node = unlocked_qs.order_by("-unlocked_at").first()
        current_skill_node = latest_node.node_key if latest_node else None
    else:
        unlocked_count = 0
        total_count = 0
        current_skill_node = None

    has_partner = AccountabilityPartnership.objects.filter(
        is_active=True
    ).filter(Q(player_one=player) | Q(player_two=player)).exists()

    singular_goal_value = None
    if is_own and singular_goal:
        singular_goal_value = singular_goal.title

    return {
        "xp_multiplier": float(multiplier.multiplier) if multiplier else 1.0,
        "singular_goal": singular_goal_value,
        "unlocked_skill_nodes": unlocked_count,
        "total_skill_nodes": total_count,
        "current_skill_node": current_skill_node,
        "public_output_log_count": OutputLog.objects.filter(player=player, is_public=True).count(),
        "has_accountability_partner": has_partner,
    }


_PATH_BUILDERS = {
    "fitness_warrior": lambda player, is_own: (_fitness_summary(player), []),
    "mindset_sage": lambda player, is_own: (
        _mindset_summary(player, is_own=is_own),
        [] if is_own else ["dark_night_count"],
    ),
    "health_alchemist": lambda player, is_own: (_health_summary(player), []),
    "discipline_knight": lambda player, is_own: (
        _discipline_summary(player, is_own=is_own),
        [] if is_own else ["discipline_code"],
    ),
    "grind_visionary": lambda player, is_own: (
        _grind_summary(player, is_own=is_own),
        [] if is_own else ["singular_goal"],
    ),
}


def build_path_profiles(player, *, is_own):
    """Return list of path profile payloads for this player's active paths."""
    payloads = []
    for path_key in active_paths_for(player):
        builder = _PATH_BUILDERS.get(path_key)
        if builder is None:
            continue
        summary, hidden_fields = builder(player, is_own)
        payloads.append({
            "path": path_key,
            "path_label": PATH_LABELS.get(path_key, path_key.replace("_", " ").title()),
            "summary": summary,
            "visibility": {
                "is_own_profile": is_own,
                "hidden_fields": hidden_fields,
            },
        })
    return payloads


# ── BADGES & TITLES ──────────────────────────────────────────────────────────


def build_badge_summary(player, *, recent_limit=5):
    """Return badges payload split into recent badges and canonical title badges."""
    user_badges = (
        UserBadge.objects.filter(player=player)
        .select_related("badge")
        .order_by("-earned_at")
    )

    recent = []
    titles = []
    for ub in user_badges:
        badge = ub.badge
        entry_base = {
            "key": badge.key,
            "name": badge.name,
            "description": badge.description,
            "earned_at": ub.earned_at.isoformat(),
        }
        if badge.key in CROSS_PATH_TITLE_KEYS:
            titles.append(entry_base)
        else:
            recent.append({**entry_base, "tier": badge.tier})

    return {
        "count": user_badges.count(),
        "recent": recent[:recent_limit],
        "titles": titles,
    }


def build_achievement_cards(player, *, limit=5):
    """Compact recent achievement cards. Drops freeform metadata."""
    cards = AchievementCard.objects.filter(player=player).order_by("-earned_at")[:limit]
    return [
        {
            "id": card.id,
            "title": card.title,
            "subtitle": card.subtitle,
            "card_type": card.card_type,
            "earned_at": card.earned_at.isoformat(),
        }
        for card in cards
    ]


# ── TOP-LEVEL ASSEMBLER ──────────────────────────────────────────────────────


def build_public_profile_extensions(player, *, is_own):
    """Return the dict of new top-level fields appended to the public profile."""
    return {
        "path_profiles": build_path_profiles(player, is_own=is_own),
        "badges": build_badge_summary(player),
        "achievement_cards": build_achievement_cards(player),
    }
