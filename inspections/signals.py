from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from data.models import Notification
from inspections.models import Inspection


@receiver(post_save, sender=Inspection, dispatch_uid="create_inspection_notification")
def send_inspection_notification(sender, instance, **kwargs):
    datetime_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    message = f'{datetime_now} {instance.deck.designator} {instance.type}: {instance.status.title}.'

    Notification.objects.create(user=instance.user_assigned, text=message)
    if instance.user_assigned.id != instance.scheduled_by.id:
        # send if it's different user
        Notification.objects.create(user=instance.scheduled_by, text=message)
