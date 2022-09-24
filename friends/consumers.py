import json
from django.db.models import Q
from django.utils.translation import gettext as _
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from accounts.models import User
from .models import FriendList, FriendRequest

    

class FriendConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def online(self):
        username = self.scope['user'].username
        if self.room_name == username:
            userModel = User.objects.filter(username=username).first()
            if userModel: 
                userModel.is_online = True
                userModel.save()

    @sync_to_async
    def offline(self):
        username = self.scope['user'].username
        if self.room_name == username:
            userModel = User.objects.filter(username=username).first()
            if userModel: 
                userModel.is_online = False
                userModel.save()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'friends_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.online()

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.offline()

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        username = data['username']

        response = await self.save_friend_request(username)

        if type(response) == type(str()):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'error',
                    'email': user.email,
                    'error': response,
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'friend_request',
                    'sender_hash': response['sender_hash'],
                    'sender_username': response['sender_username'],
                    'sender_email': response['sender_email'],
                    'sender_image': response['sender_image'],
                    'receiver_email': response['receiver_email'],
                    'receiver_image': response['receiver_image'],
                }
            )

    async def friend_request(self, event):
        sender_hash = event['sender_hash']
        sender_username = event['sender_username']
        sender_email = event['sender_email']
        sender_image = event['sender_image']
        receiver_email = event['receiver_email']
        receiver_image = event['receiver_image']

        await self.send(text_data=json.dumps({
            'type': "friend_request",
            'sender_hash': sender_hash,
            'sender_username': sender_username,
            'sender_email': sender_email,
            'sender_image': sender_image,
            'receiver_email': receiver_email,
            'receiver_image': receiver_image,
        }))

    async def error(self, event):
        email = event['email']
        error = event['error']

        await self.send(text_data=json.dumps({
            'type': "error",
            'email': email,
            'error': error,
        }))

    async def friend_accept(self, event):
        email = event['email']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': "friend_accept",
            'email': email,
            'username': username,
        }))

    async def friend_decline(self, event):
        email = event['email']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': "friend_decline",
            'email': email,
            'username': username,
        }))

    @sync_to_async
    def save_friend_request(self, username):
        user = self.scope['user']
        friend = User.objects.filter(username=username).first()
        error = None

        if friend:
            if friend != user:
                request = FriendRequest.objects.filter(Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user)).first()
                if not request:
                    FriendRequest.objects.create(sender=user, receiver=friend)
                elif request.is_active and request.sender == user:
                    error = _("You have already sent this user a friend request.")
                elif not request.is_active:
                    error = _("You are already friends with this user")
                else:
                    error = _("You already have a friend request from this user")
            else:
                error = _("You cannot send yourself a friend request.")
        else:
            error = _("Please enter a valid username.")

        if error:
            return error
        else: 
            return {
                'sender_hash': user.hash,
                'sender_username': user.username,
                'sender_email': user.email,
                'sender_image': user.image.url,
                'receiver_email': friend.email,
                'receiver_image': friend.image.url,
            }