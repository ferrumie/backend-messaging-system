"""
ASGI config for messaging_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from api.routing import websocket_urlpatterns
from message_app.middleware import JWTWebsocketMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_system.settings')

application = get_asgi_application()

application = ProtocolTypeRouter(
    {"http": application, "websocket": JWTWebsocketMiddleware(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))}
)
