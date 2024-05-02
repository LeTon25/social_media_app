import base64
import os
from django.utils.timesince import timesince

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

import json

from facebook_prj import settings
from userauths.models import Profile, User
from core.models import ChatMessage, GroupChat, GroupChatMessage

from datetime import datetime
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
    
    def get_extension_from_bytes_data(self,bypes_data : str):
        header  = bypes_data.split(',')[0].split(';')[0]
        splashIndex = header.find('/')

        return header[splashIndex+1:]

    def process_image(self,bytes_data):
        extension = self.get_extension_from_bytes_data(bypes_data=str(bytes_data))
        bytes_data = bytes_data.replace(f'data:image/{extension};base64,','')
        image_data = base64.b64decode(bytes_data)
        uploads_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/images')   
        current_datetime_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') 
        fileName = current_datetime_str +'.'+ extension
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)
        file_path = os.path.join(uploads_folder, fileName)
        with open(file_path, 'wb') as file:
            file.write(image_data)
        return fileName

    
    def process_file(self,file_name,file_data):
        extension = self.get_extension_from_bytes_data(bypes_data=str(file_data))
        file_data = file_data.replace(f'data:application/{extension};base64,','')
        content = base64.b64decode(file_data)
        uploads_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/files')   
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)
        file_path = os.path.join(uploads_folder, file_name)
        with open(file_path, 'wb') as file:
            file.write(content)

        
    def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        print("==================== message_type = ", message_type)
        print(data)
        message = data.get('message')
        sender_username = data.get('sender')
        image = data.get('image')
        imageName= ''
        file_data = data.get('file_doc')
        file_name = data.get('file_name')
        try:
            sender = User.objects.get(username=sender_username)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.image.url
            if(len(image) >0):
                imageName =  self.process_image(image)
            if (len(file_name) > 0 and len(file_data) > 0):
                self.process_file(file_name,file_data)
                #print(file_data)
        except User.DoesNotExist:
            profile_image = ''

        if message_type == 'chat_message':
            message = data.get('message')
            sender_username = data.get('sender')
            image = data.get('image')
            imageName= ''
            file_data = data.get('file_doc')
            file_name = data.get('file_name')
            try:
                sender = User.objects.get(username=sender_username)
                profile = Profile.objects.get(user=sender)
                profile_image = profile.image.url
                if(len(image) >0):
                    imageName =  self.process_image(image)
                if (len(file_name) > 0 and len(file_data) > 0):
                    self.process_file(file_name,file_data)
                    #print(file_data)
            except User.DoesNotExist:
                profile_image = ''

            reciever = User.objects.get(username=data['reciever'])
            chat_message = ChatMessage(
                sender=sender,
                reciever=reciever,
                message=message,
                image_paths = imageName,
                file_paths = file_name
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
                    'image_paths' : imageName,
                    'file_paths' : file_name,
                }
            )
        elif message_type == 'video-call':
            # Gửi thông báo cuộc gọi đến người dùng cụ thể
            self.handle_video_call(data)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
    
    def handle_video_call(self, data):
        # Lấy thông tin người gửi và người nhận từ dữ liệu
        sender_username = data.get('sender')
        receiver_username = data.get('receiver_name')
        print("==================== sender = ", sender_username)
        print("==================== receiver = ", receiver_username)

        # Kiểm tra xem người dùng có tồn tại không
        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)
            print("==================== sender = ", sender)
            print("==================== receiver = ", receiver)
        except User.DoesNotExist:
            print("Một trong các người dùng không tồn tại.")
            return
        
        # Gửi thông báo cuộc gọi đến bên nhận
        async_to_sync(self.channel_layer.group_send)(
            f'chat_{receiver_username}', 
            {
                'type': 'incoming_video_call',
                'from': sender_username
            }
        )

        # Gửi thông báo cuộc gọi đến bên gọi
        async_to_sync(self.channel_layer.group_send)(
            f'chat_{sender_username}', 
            {
                'type': 'outgoing_video_call',
                'to': receiver_username,
                'from': sender_username
            }
        )

    def video_call(self, event):
        # Gửi thông báo cuộc gọi đến người dùng thông qua WebSocket
        # Gửi thông báo cuộc gọi đến người dùng thông qua WebSocket
        self.send(text_data=json.dumps({
            'type': 'video_call',
            'call_type': 'incoming',
            'from': event['from']
        }))

    def incoming_video_call(self, event):
        sender = event['from']
        # Hiển thị thông báo cuộc gọi đến trên bên nhận
        self.send(text_data=json.dumps({
            'type': 'incoming_video_call',
            'from': sender
        }))

    def outgoing_video_call(self, event):
        receiver = event['to']
        sender = event['from']
        # Mở cửa sổ video call trên bên gọi
        self.send(text_data=json.dumps({
            'type': 'outgoing_video_call',
            'to': receiver,
            'from': sender
        }))

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


class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'notify-call-incoming':
            # Gửi thông báo đến người dùng bên kia
            await self.channel_layer.group_send(
                "call_group",
                {
                    'type': 'call.incoming',
                    'callerId': text_data_json['callerId']
                }
            )

    async def call_incoming(self, event):
        # Gửi thông báo đến người dùng bên kia
        await self.send(text_data=json.dumps({
            'type': 'call-incoming',
            'callerId': event['callerId']
        }))