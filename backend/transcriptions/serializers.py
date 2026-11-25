from rest_framework import serializers

from .models import Transcription


class TranscriptionSerializer(serializers.ModelSerializer):
    """Converts Transcription <-> JSON and validates incoming data."""

    class Meta:
        model = Transcription
        fields = ["id", "text", "language", "duration_sec", "created_at", "updated_at"]
        # Server-controlled; clients can't set these.
        read_only_fields = ["id", "created_at", "updated_at"]
