from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json

from .models import Notification



class NotificationConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_notification(self, message, author):
        return Notification.objects.create(content=message, user_id=author)
    
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
        author = text_data_json["author"]
        user_id = text_data_json["user_id"]

        event = {
            'type': 'send_message',
            'message': message,
            "author" : author,
            "user_id" : user_id
        }

# 그룹에 메시지 보내기
        await self.channel_layer.group_send(self.room_name, event)
        print(author)
        print(user_id)
        print(type(author))
        print(type(user_id))

        if int(author) != user_id :
            save_message = await self.create_notification(message=message, author = author)
    # 그룹에서 메시지 받기
    async def send_message(self, event):
        message = event["message"]
        author = event["author"]
        user_id = event["user_id"]

        # 웹소켓에 메시지 보내기
        await self.send(text_data=json.dumps({'message': message, 'author' : author, "user_id":user_id}))