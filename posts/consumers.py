import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from accounts.models import User
from .models import Post, PostComment


class PostCommentConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'posts_%s' % self.room_name

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
        type = data['type']
        userName = self.scope['user'].username

        if type == 'comment_post':
            content = data['content']
            sentDateTime = await self.save_comment(content)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'post_comment',
                    'content': content,
                    'userName': userName,
                    'sentDateTime': sentDateTime,
                }
            )
        elif type == 'like_post':
            rates = await self.like_post()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'post_like',
                    'rates': rates,
                }
            )
        elif type == 'dislike_post':
            rates = await self.dislike_post()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'post_dislike',
                    'rates': rates,
                }
            )

    async def post_like(self, event):
        rates = event['rates']
        await self.send(text_data=json.dumps({
            'type': 'post_like',
            'likes': rates[0],
            'dislikes': rates[1],
        }))
        
    async def post_dislike(self, event):
        rates = event['rates']
        await self.send(text_data=json.dumps({
            'type': 'post_dislike',
            'likes': rates[0],
            'dislikes': rates[1],
        }))

    async def post_comment(self, event):
        content = event['content']
        userName = event['userName']
        sentDateTime = event['sentDateTime']
        image = self.scope['user'].image.url

        await self.send(text_data=json.dumps({
            'type': 'post_comment',
            'content': content,
            'userName': userName,
            'senderImage': image,
            'sentDateTime': sentDateTime,
        }, indent=4, sort_keys=True, default=str))

    @sync_to_async
    def like_post(self):
        post = Post.objects.filter(hash=self.room_name).first()
        post.add_liked_user(self.scope['user'])
        return [post.liked_users.all().count(), post.disliked_users.all().count()]

    @sync_to_async
    def dislike_post(self):
        post = Post.objects.filter(hash=self.room_name).first()
        post.add_disliked_user(self.scope['user'])
        return [post.liked_users.all().count(), post.disliked_users.all().count()]

    @sync_to_async
    def save_comment(self, content):
        sentDateTime = None
        post = Post.objects.filter(hash=self.room_name).first()

        if content and post:
            comment = PostComment.objects.create(
                user=self.scope['user'], 
                content=content
            )

            post.add_comment(comment)
            sentDateTime = comment.sent_date_time

        return sentDateTime