"""Open-source speech-to-text via faster-whisper (multilingual; handles Hindi+English code-mixing)."""
import os
import threading
import numpy as np
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
_model = None
_lock = threading.Lock()

# Prompt nudges Whisper to keep English words as English inside Hindi speech.
INITIAL_PROMPT = "Hindi and English mixed conversation. हिंदी और English मिश्रित बातचीत।"


def get_model() -> WhisperModel:
    global _model
    with _lock:
        if _model is None:
            _model = WhisperModel(
                os.getenv("WHISPER_MODEL", "small"),
                device=os.getenv("WHISPER_DEVICE", "cpu"),
                compute_type=os.getenv("WHISPER_COMPUTE", "int8"),
            )
        return _model


def transcribe(pcm16: bytes, language: str | None = None) -> tuple[str, str]:
    """Transcribe 16kHz mono int16 PCM. language=None means auto-detect."""
    if len(pcm16) < SAMPLE_RATE * 2 * 0.4:  # under 0.4s
        return "", language or ""
    audio = np.frombuffer(pcm16, dtype=np.int16).astype(np.float32) / 32768.0
    model = get_model()
    with _lock:
        segments, info = model.transcribe(
            audio,
            language=language,
            task="transcribe",
            beam_size=1,
            vad_filter=True,
            # Lower threshold so quiet / speaker-played speech isn't discarded as silence.
            vad_parameters={"threshold": 0.25, "min_silence_duration_ms": 700},
            condition_on_previous_text=False,
            # Hindi/English hint only for those languages (or auto); it would bias others like Tamil.
            initial_prompt=INITIAL_PROMPT if language in (None, "hi", "en") else None,
        )
        text = " ".join(s.text.strip() for s in segments).strip()
    return text, info.language
