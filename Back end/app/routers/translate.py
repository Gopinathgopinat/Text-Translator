from fastapi import APIRouter
from app.models.schemas import TranslateRequest, TranslateResponse, Language
from app.services.translator import translate_text, get_languages
from typing import List

router = APIRouter()


@router.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translate text from source language to target language.
    Set source_lang to 'auto' for automatic language detection.
    """
    result = await translate_text(
        text=request.text,
        source=request.source_lang,
        target=request.target_lang
    )

    return TranslateResponse(
        translated_text=result.get("translatedText", ""),
        source_lang=request.source_lang,
        target_lang=request.target_lang,
        detected_language=result.get("detectedLanguage", {}).get("language") if isinstance(result.get("detectedLanguage"), dict) else result.get("detectedLanguage")
    )


@router.get("/languages", response_model=List[Language])
async def languages():
    """
    Get all supported translation languages.
    """
    raw = await get_languages()
    return [Language(code=lang["code"], name=lang["name"]) for lang in raw]
