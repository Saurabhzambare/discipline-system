from django.contrib import admin

from .models import (
    ActivityEvent,
    FriendRequest,
    Friendship,
    GroupMembership,
    PostComment,
    PostReaction,
    SocialGroup,
    SocialPost,
)

admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(SocialPost)
admin.site.register(PostComment)
admin.site.register(PostReaction)
admin.site.register(ActivityEvent)
admin.site.register(SocialGroup)
admin.site.register(GroupMembership)
