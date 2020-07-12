from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User, dispatch_uid="user_password")
def check_password(sender, instance, **kwargs):
    password_is_hashed = bool(
        'pbkdf2_sha256' in instance.password and
        str(instance.password).count('$') == 3
    )
    if not password_is_hashed:
        instance.set_password(instance.password)
        instance.save()
