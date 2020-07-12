from django.contrib.postgres.fields import JSONField
from django.db import models
from accounts.models import User


class CheckResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'CheckResults'


class SchemaDefinitions(models.Model):
    name = models.TextField()
    data = JSONField()

    class Meta:
        verbose_name_plural = 'SchemaDefinitions'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = JSONField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
