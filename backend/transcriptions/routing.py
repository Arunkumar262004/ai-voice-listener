"""WebSocket routes for this app (Django Channels).

urls.py only understands HTTP, so WebSocket paths are registered here instead.
config/asgi.py sends every "websocket" connection to this list; each path maps to a
consumer (consumers.py), which plays the role a view plays for HTTP.
"""
from django.urls import path

from .consumers import TranscribeConsumer

websocket_urlpatterns = [
    # ws://host/ws/transcribe?lang=auto|hi|en  -> live speech-to-text stream
    path("ws/transcribe", TranscribeConsumer.as_asgi()),
]
