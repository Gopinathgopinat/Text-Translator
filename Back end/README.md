# LinguaSwift — Text Translator Web App

Full-stack translation app built with Google Stitch (UI) + FastAPI + LibreTranslate.

## Quick Start

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API runs at http://localhost:8000
Swagger docs at http://localhost:8000/docs

### Frontend
Open frontend/index.html in a browser, or serve with:
```bash
cd frontend
python -m http.server 3000
```

## Deployment (Render)
- Backend: Web Service → Root: backend → Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
- Frontend: Static Site → Root: frontend
- Set env var: LIBRE_TRANSLATE_URL, LIBRE_API_KEY, ALLOWED_ORIGINS
