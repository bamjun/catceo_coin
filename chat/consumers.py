import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import BaseFirstChat
from asgiref.sync import sync_to_async
import pytz

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'chat_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'chat_group',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        nickname = data['nickname']
        content = data['content']

        chat = await sync_to_async(BaseFirstChat.objects.create)(
            nickname=nickname,
            content=content
        )

        await self.channel_layer.group_send(
            'chat_group',
            {
                'type': 'chat_message',
                'nickname': nickname,
                'content': content,
                'timestamp': chat.time.astimezone(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S %Z')
            }
        )

    async def chat_message(self, event):
        nickname = event['nickname']
        content = event['content']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'nickname': nickname,
            'content': content,
            'timestamp': timestamp
        }))
