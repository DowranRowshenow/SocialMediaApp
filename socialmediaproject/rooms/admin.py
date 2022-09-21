from django.contrib import admin

from .models import Message, Room


class RoomAdmin(admin.ModelAdmin):
    list_filter = ['user1', 'user2', 'token']
    list_display = ['user1', 'user2', 'token']
    search_fields = ['user1', 'user2', 'token']

    class Meta:
        model = Room

admin.site.register(Room, RoomAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'room', 'content']
    list_display = ['sender', 'room', 'content']
    search_fields = ['sender__email', 'room', 'content']

    class Meta:
        model = Message

admin.site.register(Message, MessageAdmin)