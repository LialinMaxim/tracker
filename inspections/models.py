from datetime import date

from django.db import models
from django.contrib.postgres.fields import JSONField

from accounts.models import User
from decks.models import Deck


class Status(models.Model):
    title = models.CharField(max_length=16)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Statuses'


class InspectionType(models.Model):
    title = models.CharField(max_length=32)
    updated = models.DateTimeField(auto_now=True, editable=False)
    schema = JSONField(blank=True, default=dict)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "inspection_type"


class Inspection(models.Model):
    author = models.ForeignKey(User, related_name='inspection_author', on_delete=models.CASCADE)
    user_assigned = models.ForeignKey(User, related_name='inspection_assigned', on_delete=models.CASCADE)
    scheduled_by = models.ForeignKey(User, related_name='inspection_scheduled_by', on_delete=models.CASCADE)
    completed_by = models.ForeignKey(User, related_name='inspection_completed_by', on_delete=models.CASCADE,
                                     null=True, blank=True)
    status = models.ForeignKey(Status, related_name='inspection', on_delete=models.CASCADE)
    type = models.ForeignKey(InspectionType, related_name='inspection', on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, related_name='inspection', on_delete=models.CASCADE)
    due_date = models.DateField(default=date.today)
    completed_date = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, editable=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f'Inspection {self.pk} {self.type}'

    class Meta:
        ordering = ('-updated',)


class Report(models.Model):
    inspection = models.ForeignKey(Inspection, related_name='report', on_delete=models.CASCADE)
    groups = JSONField(blank=False, null=False)
    groups_preview = JSONField(blank=True, null=False)
    colors_set = models.TextField(blank=True, null=False)
    values_set = models.TextField(blank=True, null=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
