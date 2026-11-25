from django.db import models


class Transcription(models.Model):
    """One saved speech-to-text result (table: transcriptions_transcription)."""

    text = models.TextField()  # transcribed (possibly Hindi + English mixed) text
    language = models.CharField(max_length=16, blank=True, null=True)  # detected code, e.g. "hi"
    duration_sec = models.FloatField(blank=True, null=True)  # length of the audio
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # set once on insert
    updated_at = models.DateTimeField(auto_now=True)  # refreshed on every save/edit

    class Meta:
        ordering = ["-created_at"]  # newest first by default

    def __str__(self):
        return f"{self.id}: {self.text[:40]}"
