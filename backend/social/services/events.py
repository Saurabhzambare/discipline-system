"""Helpers for creating ActivityEvent records consistently across the codebase."""

from social.models import ActivityEvent


def create_activity_event(
    *,
    actor,
    event_type,
    text_snapshot,
    related_post=None,
    related_player=None,
    related_group=None,
    is_public=True,
):
    """Create an ActivityEvent using only fields the model actually supports.

    The model has no JSON metadata field, so callers must encode any extra
    context into ``text_snapshot`` or the supported related_* foreign keys.
    """
    return ActivityEvent.objects.create(
        actor=actor,
        event_type=event_type,
        text_snapshot=text_snapshot[:255],
        related_post=related_post,
        related_player=related_player,
        related_group=related_group,
        is_public=bool(is_public),
    )
