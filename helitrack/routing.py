from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from .channelsmiddleware import TokenAuthMiddleware

from data import consumers

application = ProtocolTypeRouter({

    "websocket": TokenAuthMiddleware(
        URLRouter([
            url('notifications', consumers.NotificationsConsumer),
        ])
    )

})
