import json
from datetime import date

from django.core.exceptions import ValidationError

from helitrack.settings.common import REPORT_COLOR, REPORT_VALUES, REPORT_TARGET_VALUES


def validate_future_date(value):
    if value < date.today():
        raise ValidationError("Due date can be in past")
    return value


def validate_groups(groups):
    if not groups:
        raise ValidationError(f"Data is not JSON:{groups}")

    try:
        validate_groups = json.loads(groups)
    except BaseException as err:
        raise ValidationError(f"Groups could not load to Dict: {err}")

    groups_preview = []
    values = []
    for k, v in dict(validate_groups).items():
        if isinstance(v, dict):
            groups_preview.append(
                v.get(REPORT_COLOR) or
                v.get(REPORT_COLOR.lower())
            )
            values.extend(
                v.get(REPORT_VALUES, {}).values() or
                v.get(REPORT_VALUES.title(), {}).values()
            )
        else:
            raise ValidationError(f"Value must be a Dict: {v}")
    colors_set = ' '.join(set(map(str, groups_preview))).lower()
    values_set = ' '.join(
        [value for value in set(map(str, values)) if value in REPORT_TARGET_VALUES]
    ).lower()
    return validate_groups, groups_preview, colors_set, values_set
