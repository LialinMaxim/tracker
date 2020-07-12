from django.db import close_old_connections
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()

        try:
            # get token
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

            # decrypt token
            decoded_data = jwt_decode_handler(token)

            # get user
            user = get_user_model().objects.get(id=decoded_data["user_id"])
        except:
            return self.inner(dict(scope, user=None))

        return self.inner(dict(scope, user=user))
