import os

from django.core.exceptions import ValidationError
from django.utils import timezone

from helitrack.settings.common import MEDIA_DECK


def validate_photo_size(image_file):
    if image_file.size > 5242880:
        raise ValidationError("The maximum image file size that can be uploaded is 5MB")
    else:
        return image_file


def deck_photo_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    new_filename = timezone.now()
    return f'{MEDIA_DECK}{new_filename}{file_extension}'


def validate_position_latitude(position):
    position = round(position, 5)
    if -90 <= position <= 90:
        return position
    raise ValidationError("Latitude must be a float between -90 and 90 degrees")


def validate_position_longitude(position):
    position = round(position, 5)
    if -180 <= position <= 180:
        return position
    raise ValidationError("Longitude must be a float between -180 and 180 degrees")
