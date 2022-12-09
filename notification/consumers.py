from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json

from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_notification(self, message):
        return Notification.objects.create(content=message)

    async def connect(self):
        self.group_name = 'notification'

        # 그룹 참가
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, cocde):
        # 그룹 떠남
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # 웹소켓에서 메시지 받기

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        event = {
            'type': 'send_message',
            'message': message
        }

# 그룹에 메시지 보내기
        await self.channel_layer.group_send(self.group_name, event)
        save_message = await self.create_notification(message=message)

    # 그룹에서 메시지 받기
    async def send_message(self, event):
        message = event["message"]

        # 웹소켓에 메시지 보내기
        await self.send(text_data=json.dumps({'message': message}))
