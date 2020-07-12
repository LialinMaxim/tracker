from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate


class IsUsedValidator:

    def validate(self, password, user=None):

        check_user = authenticate(username=user.username, password=password)

        if check_user is None:
            return
        else:
            raise ValidationError(
                _("You can't use your previous password"),
                code='password_already_used_by_you'
            )

    def get_help_text(self):
        return _(
            "You can't use your previous password"
        )