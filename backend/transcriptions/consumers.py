"""WebSocket real-time transcription.

Client sends binary 16kHz mono int16 PCM frames; text "stop" finalizes and saves.
Server replies JSON: {type: partial|final, text, language, id?}.
"""
import asyncio
import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from . import stt
from .models import Transcription

PARTIAL_EVERY_SEC = 1.5
MAX_BUFFER_SEC = 30
BYTES_PER_SEC = stt.SAMPLE_RATE * 2


class TranscribeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        qs = parse_qs(self.scope["query_string"].decode())
        lang = qs.get("lang", ["auto"])[0]
        self.language = None if lang in ("", "auto") else lang
        self.buf = bytearray()
        self.last_len = 0
        self.busy = asyncio.Lock()  # one transcription at a time per connection
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.buf.extend(bytes_data)
            if len(self.buf) > MAX_BUFFER_SEC * BYTES_PER_SEC:
                await self._finalize()  # auto-commit very long utterances
            elif (
                len(self.buf) - self.last_len >= PARTIAL_EVERY_SEC * BYTES_PER_SEC
                and not self.busy.locked()
            ):
                self.last_len = len(self.buf)
                async with self.busy:
                    text, lang = await self._transcribe(bytes(self.buf))
                await self.send(json.dumps({"type": "partial", "text": text, "language": lang}))
        elif text_data == "stop":
            await self._finalize()

    async def _transcribe(self, data):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, stt.transcribe, data, self.language)

    async def _finalize(self):
        data = bytes(self.buf)
        self.buf.clear()
        self.last_len = 0
        async with self.busy:
            text, lang = await self._transcribe(data)
        out = {"type": "final", "text": text, "language": lang}
        if text:
            obj = await database_sync_to_async(Transcription.objects.create)(
                text=text, language=lang, duration_sec=len(data) / BYTES_PER_SEC
            )
            out["id"] = obj.id
        await self.send(json.dumps(out))
