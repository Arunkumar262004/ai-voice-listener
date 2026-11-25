"""ASGI entry point: the single place where traffic is split by protocol.

  HTTP       -> normal Django (config/urls.py -> transcriptions/urls.py -> views.py)
  WebSocket  -> Channels router (transcriptions/routing.py -> consumers.py)
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# Must run before importing any app code that touches models/settings.
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from transcriptions.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
