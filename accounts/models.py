from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _

from decks.models import Operator, Cluster
from helitrack.settings.common import INSPECTOR_NAME


class User(AbstractUser):
    payment_info = JSONField(default=dict, blank=True)
    alias = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    vessel = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    operator = models.ForeignKey(Operator, related_name='user', on_delete=models.CASCADE, null=True)
    clusters = models.ManyToManyField(Cluster, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'alias', 'vessel', 'description']

    def __str__(self):
        return self.email

    def is_administer(self):
        admin_group_id = GroupLevel.objects.order_by('level').last().group.id
        user_groups_ids = [group.id for group in self.groups.all()]
        return admin_group_id in user_groups_ids

    def is_inspector(self):
        is_inspector = [INSPECTOR_NAME in str(group.name).lower() for group in self.groups.all()]
        if True in is_inspector:
            return True


class GroupLevel(models.Model):
    level = models.PositiveSmallIntegerField(unique=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group} - {self.level}'
