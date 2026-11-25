# AI Voice Listener – Real-time Speech to Text

Multilingual (Hindi + English) real-time transcription with a CRUD history dashboard.

- **Frontend:** React (Vite). Mic -> AudioWorklet (16 kHz PCM) -> WebSocket
- **Backend:** Django + Django REST Framework (CRUD in `views.py`), Django Channels (WebSocket consumer)
- **STT:** `faster-whisper` (open-source, self-hosted, auto language detect)
- **DB:** PostgreSQL

## Run

```bash
# 1. Postgres (installed locally) - create DB and user once, in psql:
#    CREATE USER voice WITH PASSWORD 'voice' CREATEDB;
#    CREATE DATABASE voicedb OWNER voice;

# 2. Backend
cd backend
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000   # serves HTTP + WebSocket via daphne

# 3. Frontend
cd frontend
npm install
npm run dev     # http://localhost:5173
```

Env vars (backend): `POSTGRES_DB/USER/PASSWORD/HOST/PORT`, `WHISPER_MODEL` (tiny/base/small/medium), `WHISPER_DEVICE`, `WHISPER_COMPUTE`, `CORS_ORIGINS`.

## API
`GET/POST /api/transcriptions`, `GET/PUT/DELETE /api/transcriptions/{id}`, `WS /ws/transcribe?lang=auto|hi|en`
