from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import translate
import os

app = FastAPI(
    title="LinguaSwift API",
    description="Text translation API powered by LibreTranslate",
    version="1.0.0"
)

# ── CORS ──────────────────────────────────────────────────────────────────
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:5500").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change to allowed_origins in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── ROUTES ─────────────────────────────────────────────────────────────────
app.include_router(translate.router, prefix="/api/v1", tags=["translation"])

@app.get("/")
async def root():
    return {"message": "LinguaSwift API is running", "docs": "/docs"}
