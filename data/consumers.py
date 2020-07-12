import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .serializers import NotificationSerializer
from .models import Notification


NOTIFICATIONS_TO_RETURN = 10


class NotificationsConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]

        if self.user is None:
            return self.close()

        self.accept()

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        notifications = Notification.objects.filter(
            user=self.user
        ).order_by('-created_at')[:NOTIFICATIONS_TO_RETURN]

        all_count = Notification.objects.filter(user=self.user).count()
        unread_count = Notification.objects.filter(user=self.user, is_read=False).count()
        data_to_send = list(map(lambda x: NotificationSerializer(x).data, notifications))

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'notifications',
                'data': data_to_send,
                'all_count': all_count,
                'unread_count': unread_count
            }
        )

    def disconnect(self, code):
        if self.user:
            async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
 
    @property
    def group_name(self):
        return self.get_user_group_name(self.user)

    @staticmethod
    def get_user_group_name(user):
        return f'user-{user.id}'

    def notifications(self, event):
        self.send(json.dumps(event))

    def notification(self, event):
        self.send(json.dumps(event))
