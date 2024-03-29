from django.contrib import admin

from .models import (
    UserProfile,
    ContactMessage,
    FriendList,
    FriendRequest,
    Notification,
    Message,
)


admin.site.register(UserProfile)
admin.site.register(ContactMessage)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Notification)
