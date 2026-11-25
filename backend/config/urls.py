"""Project-level HTTP routes: everything REST lives under /api/."""
from django.urls import include, path

urlpatterns = [
    path("api/", include("transcriptions.urls")),  # delegate to the app's urls.py
]
