import asyncio
from fastapi import HTTPException
from deep_translator import GoogleTranslator
from deep_translator.exceptions import (
    TranslationNotFound,
    LanguageNotSupportedException,
    RequestError,
    TooManyRequests,
)
from typing import Optional


# ── Language list (built once at import, no network needed) ─────────────────
def _build_language_list() -> list:
    """
    Returns [{code, name}] sorted alphabetically by name.
    deep-translator returns {name: code}, so we flip and title-case the name.
    """
    raw = GoogleTranslator(source="auto", target="en").get_supported_languages(as_dict=True)
    return sorted(
        [{"code": code, "name": name.title()} for name, code in raw.items()],
        key=lambda x: x["name"],
    )

LANGUAGES = _build_language_list()   # 133 languages, cached in memory


# ── Core translation ────────────────────────────────────────────────────────
async def translate_text(text: str, source: str, target: str) -> dict:
    """
    Translate text using GoogleTranslator (deep-translator).
    Runs the synchronous call in a thread pool so FastAPI stays non-blocking.

    Returns:
        {
            "translatedText": str,
            "detectedLanguage": str | None   # only when source == "auto"
        }
    """
    def _sync_translate():
        translator = GoogleTranslator(source=source, target=target)
        return translator.translate(text)

    try:
        translated = await asyncio.get_event_loop().run_in_executor(None, _sync_translate)

        if translated is None:
            raise HTTPException(status_code=502, detail="Translation returned empty result.")

        return {
            "translatedText": translated,
            "detectedLanguage": None,   # GoogleTranslator doesn't expose detected lang directly
        }

    except LanguageNotSupportedException:
        raise HTTPException(
            status_code=400,
            detail=f"Language not supported. Source: '{source}', Target: '{target}'."
        )

    except TranslationNotFound:
        raise HTTPException(
            status_code=404,
            detail="No translation found for the given text."
        )

    except TooManyRequests:
        raise HTTPException(
            status_code=429,
            detail="Too many requests to Google Translate. Please wait a moment and try again."
        )

    except RequestError:
        raise HTTPException(
            status_code=503,
            detail="Cannot reach Google Translate. Check your internet connection."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )


# ── Language list ────────────────────────────────────────────────────────────
async def get_languages() -> list:
    """
    Returns the cached list of 133 supported languages.
    No network call required — deep-translator has the list built in.
    """
    return LANGUAGES


# ── Language detection (optional helper) ───────────────────────────────────
async def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of a text snippet using deep-translator's
    single_detection helper (requires langdetect package).
    Returns the language code string, or None on failure.
    """
    try:
        from deep_translator import single_detection
        def _detect():
            return single_detection(text, api_key=None)
        return await asyncio.get_event_loop().run_in_executor(None, _detect)
    except Exception:
        return None
