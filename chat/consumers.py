from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message
from django.contrib.auth.models import User
import json


class ChatConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def save_message(self, message):
        print('message saving')
        sender = message.get('sender')
        receiver = message.get('receiver')
        mm = message.get('message')
        msg = Message.objects.create(
            sender_id=sender.get('id'),
            receiver_id=receiver.get('id'),
            message=mm
        )
        message.update({'msg_time': msg.create_date.strftime("%b %d, %Y, %H:%M %p")})


    async def connect(self):
        group_name = self.scope.get('query_string').decode('utf-8').split('=')[-1]
        self.room_group_name = 'chat_%s' % group_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # save message in database
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
