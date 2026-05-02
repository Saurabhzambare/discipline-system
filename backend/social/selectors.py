"""Read-only query helpers for social domain."""

from django.db.models import Count, Q

from .models import ActivityEvent, AchievementCard, Friendship, GroupMembership, SocialGroup, SocialPost, UserBadge


def friend_ids_for_player(*, player):
    """Return friend player ids for the given player."""
    friendship_qs = Friendship.objects.filter(Q(player_one=player) | Q(player_two=player))
    friend_ids = []
    for friendship in friendship_qs.values("player_one_id", "player_two_id"):
        friend_ids.append(
            friendship["player_two_id"] if friendship["player_one_id"] == player.id else friendship["player_one_id"]
        )
    return friend_ids


def visible_posts_queryset_for_player(*, player):
    """Newest-first posts visible to the player based on simple visibility rules."""
    friend_ids = friend_ids_for_player(player=player)

    return (
        SocialPost.objects.select_related("author__user", "group")
        .prefetch_related("comments__author__user", "reactions__player__user")
        .filter(
            Q(visibility=SocialPost.VISIBILITY_PUBLIC)
            | Q(author=player)
            | Q(visibility=SocialPost.VISIBILITY_FRIENDS_ONLY, author_id__in=friend_ids)
        )
        .order_by("-created_at")
    )


def visible_post_queryset_for_player(*, player, post_id):
    return visible_posts_queryset_for_player(player=player).filter(id=post_id)


def profile_activity_queryset(*, target_player):
    """Public activity events for a player's profile, newest-first."""
    return ActivityEvent.objects.select_related("actor__user", "related_post", "related_group").filter(
        actor=target_player,
        is_public=True,
    ).order_by("-created_at")


def profile_posts_queryset(*, target_player):
    """Recent posts for profile pages, using simple public visibility only."""
    return (
        SocialPost.objects.select_related("author__user", "group")
        .filter(author=target_player, visibility=SocialPost.VISIBILITY_PUBLIC)
        .order_by("-created_at")
    )


def visible_groups_queryset_for_player(*, player):
    """Public groups for everyone + private groups where player is a member."""
    member_group_ids = GroupMembership.objects.filter(player=player).values_list("group_id", flat=True)

    return (
        SocialGroup.objects.select_related("owner__user")
        .filter(Q(is_private=False) | Q(id__in=member_group_ids))
        .distinct()
        .order_by("name")
    )


# ── Profile extension selectors ───────────────────────────────────────────────

_CROSS_PATH_TITLE_KEYS = frozenset([
    "title_warrior_sage",
    "title_optimized_human",
    "title_complete_human",
    "title_renaissance_human",
])

_PATH_DISPLAY_NAMES = {
    "fitness_warrior": "Fitness Warrior",
    "mindset_sage": "Mindset Sage",
    "health_alchemist": "Health Alchemist",
    "discipline_knight": "Discipline Knight",
    "grind_visionary": "Grind Visionary",
}


def _user_badge_to_dict(ub):
    return {
        "key": ub.badge.key,
        "name": ub.badge.name,
        "tier": ub.badge.tier,
        "earned_at": ub.earned_at,
    }


def profile_badges_selector(*, player):
    """Return badge summary dict for a player profile."""
    user_badges = list(
        UserBadge.objects.select_related("badge")
        .filter(player=player)
        .order_by("-earned_at")
    )
    titles = [_user_badge_to_dict(ub) for ub in user_badges if ub.badge.key in _CROSS_PATH_TITLE_KEYS]
    recent = [_user_badge_to_dict(ub) for ub in user_badges if ub.badge.key not in _CROSS_PATH_TITLE_KEYS][:5]
    return {
        "total_count": len(user_badges),
        "titles": titles,
        "recent": recent,
    }


def profile_achievement_cards_selector(*, player):
    """Return the 10 most recent achievement cards for a player profile."""
    return list(AchievementCard.objects.filter(player=player).order_by("-earned_at")[:10])


def _path_own_only_data(player, path):
    """Return path-specific private config dict for profile owner view."""
    from paths.models import (
        DisciplineKnightProfile,
        FitnessWarriorProfile,
        GrindVisionaryProfile,
        HealthAlchemistProfile,
        MindsetSageProfile,
    )

    getters = {
        "fitness_warrior": lambda: FitnessWarriorProfile.objects.filter(player=player).values(
            "training_split", "primary_goal", "training_days_per_week", "experience_level"
        ).first(),
        "mindset_sage": lambda: MindsetSageProfile.objects.filter(player=player).values(
            "motivation", "daily_time_commitment", "experience_level", "archetype"
        ).first(),
        "health_alchemist": lambda: HealthAlchemistProfile.objects.filter(player=player).values(
            "primary_health_goal", "health_relationship", "focus_area"
        ).first(),
        "discipline_knight": lambda: DisciplineKnightProfile.objects.filter(player=player).values(
            "routine_level", "biggest_challenge", "structure_preference", "time_commitment"
        ).first(),
        "grind_visionary": lambda: GrindVisionaryProfile.objects.filter(player=player).values(
            "grind_focus", "experience_state", "daily_hours", "current_output_state"
        ).first(),
    }
    getter = getters.get(path)
    if not getter:
        return {}
    return getter() or {}


def profile_path_profiles_selector(*, player, is_own_profile):
    """Return path profile entries for all active paths the player is on."""
    from paths.models import UserPathSelection
    from quests.models import QuestCompletion

    active_paths: set[str] = set()
    if player.path:
        active_paths.add(player.path)

    selection = UserPathSelection.objects.filter(player=player).first()
    if selection and selection.multi_paths_active:
        active_paths.update(selection.multi_paths_active)

    if not active_paths:
        return []

    path_completions = dict(
        QuestCompletion.objects.filter(player=player, quest__path_target__in=active_paths)
        .values("quest__path_target")
        .annotate(count=Count("id"))
        .values_list("quest__path_target", "count")
    )

    result = []
    for path in sorted(active_paths):
        display_name = _PATH_DISPLAY_NAMES.get(path, path.replace("_", " ").title())
        summary = {"quests_completed": path_completions.get(path, 0)}
        own_only = _path_own_only_data(player, path) if is_own_profile else {}
        result.append({
            "path": path,
            "display_name": display_name,
            "summary": summary,
            "own_only": own_only,
        })

    return result
