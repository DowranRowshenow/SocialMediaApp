import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from accounts.models import User
from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data['content']
        image = self.scope['user'].image.url
        userName = self.scope['user'].username
        roomToken = self.scope['url_route']['kwargs']['room_name']

        message = await self.save_message(roomToken, content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': content,
                'userName': userName,
                'roomToken': roomToken,
                'image': image,
                'sent_date_time': message.sent_date_time,
            }
        )

    async def chat_message(self, event):
        content = event['content']
        userName = event['userName']
        roomToken = event['roomToken']
        image = event['image']
        sent_date_time = event['sent_date_time']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'content': content,
            'userName': userName,
            'roomToken': roomToken,
            'image': image,
            'sent_date_time': sent_date_time,
        }, indent=4, sort_keys=True, default=str))

    @sync_to_async
    def save_message(self, roomToken, content):
        room = Room.objects.filter(token=roomToken).first()
        message = None

        if content and room:
            message = Message.objects.create(
                room=room,
                sender=self.scope['user'], 
                content=content
            )

        return message