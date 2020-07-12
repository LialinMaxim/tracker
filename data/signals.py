import asyncio

from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .consumers import NotificationsConsumer
from .models import Notification
from .serializers import NotificationSerializer


@receiver(post_save, sender=Notification, dispatch_uid="create_notification")
def send_notification(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_name = NotificationsConsumer.get_user_group_name(instance.user)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification',
            'data': NotificationSerializer(instance).data
        }
    )
