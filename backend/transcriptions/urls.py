"""HTTP routes (REST API) for this app.

Mounted under /api/ by config/urls.py. Only handles normal HTTP requests;
WebSocket routes live in routing.py because Django URL config can't serve them.
"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

# SimpleRouter auto-generates list/create/retrieve/update/delete routes for the ViewSet.
# trailing_slash=False -> /api/transcriptions (matches what the React frontend calls).
router = SimpleRouter(trailing_slash=False)
router.register("transcriptions", views.TranscriptionViewSet)

urlpatterns = [
    path("health", views.health),  # simple liveness check: GET /api/health
] + router.urls
