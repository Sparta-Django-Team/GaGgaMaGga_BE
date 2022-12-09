import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from .models import Notification
from channels.db import database_sync_to_async




class NotificationConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_notification(self, message):
        return Notification.objects.create(content=message, user=self.scope["user"])
    
    async def connect(self) :
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        print(10000000)
        # 그룹 떠남
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        event = {
            'type': 'send_message',
            'message': message
        }

# 그룹에 메시지 보내기
        await self.channel_layer.group_send(self.room_name, event)
        save_message = await self.create_notification(message=message)
    # 그룹에서 메시지 받기
    async def send_message(self, event):
        message = event["message"]

        # 웹소켓에 메시지 보내기
        await self.send(text_data=json.dumps({'message': message}))