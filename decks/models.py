from django.db import models

from helitrack.settings.common import AUTH_USER_MODEL
from decks.validators import (validate_photo_size, deck_photo_path,
                              validate_position_latitude, validate_position_longitude)


class Cluster(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    is_permanent = models.BooleanField(null=True, blank=True)
    author = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title


class Operator(models.Model):
    title = models.CharField(max_length=32)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title


class Deck(models.Model):
    title = models.CharField(max_length=32)
    designator = models.CharField(max_length=16)
    d_value = models.FloatField()
    t_value = models.FloatField()
    position_latitude = models.FloatField(validators=[validate_position_latitude])
    position_longitude = models.FloatField(validators=[validate_position_longitude])
    operator = models.ForeignKey(Operator, related_name='deck', on_delete=models.CASCADE, )
    cluster = models.ForeignKey(Cluster, related_name='deck', on_delete=models.CASCADE, )
    is_manned = models.BooleanField()
    is_offshore = models.BooleanField()
    updated = models.DateTimeField(auto_now=True, editable=False)
    photo = models.ImageField(upload_to=deck_photo_path, validators=[validate_photo_size],
                              null=True, blank=True)  # need operator and cluster

    def __str__(self):
        return self.title
