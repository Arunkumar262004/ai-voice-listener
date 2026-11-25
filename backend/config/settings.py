import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Keep downloaded Whisper models inside the project drive (C: may be full).
# Override with HF_HOME env var if you want a different location.
os.environ.setdefault("HF_HOME", str(BASE_DIR / ".hf_cache"))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "daphne",  # ASGI server; makes `runserver` serve WebSockets too
    "django.contrib.contenttypes",
    "django.contrib.auth",  # required by DRF internals (even though we don't use auth)
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "channels",
    "transcriptions",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "voicedb"),
        "USER": os.getenv("POSTGRES_USER", "voice"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "voice"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

USE_TZ = True
TIME_ZONE = "UTC"
STATIC_URL = "static/"
