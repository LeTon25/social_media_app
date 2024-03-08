from django.utils.timesince import timesince

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json

from userauths.models import Profile, User
from core.models import ChatMessage, GroupChat, GroupChatMessage

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_username = data.get('sender')

        try:
            sender = User.objects.get(username=sender_username)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.image.url
        except User.DoesNotExist:
            profile_image = ''

        reciever = User.objects.get(username=data['reciever'])
        chat_message = ChatMessage(
            sender=sender,
            reciever=reciever,
            message=message,
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'profile_image': profile_image,
                'reciever': reciever.username,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))


class GroupChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data):
        data = json.loads(text_data)
        groupchat_id = data.get('groupchat_id')
        message = data.get('message')
        sender_username = data.get('sender')
        full_name = data.get('full_name')

        try:
            sender = User.objects.get(username=sender_username)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.image.url
            full_name = profile.full_name
        except User.DoesNotExist:
            profile_image = ''

        groupchat = GroupChat.objects.get(id=data['groupchat_id'])
        chat_message = GroupChatMessage(
            sender=sender,
            groupchat=groupchat,
            message=message,
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'profile_image': profile_image,
                'groupchat_id': groupchat_id,
                "full_name":full_name,
                "date":timesince(chat_message.date)
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))