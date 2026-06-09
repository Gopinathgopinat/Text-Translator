from pydantic import BaseModel, validator
from typing import Optional


class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str

    @validator("text")
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        if len(v) > 5000:
            raise ValueError("Text exceeds 5000 character limit")
        return v

    @validator("target_lang")
    def target_must_not_be_auto(cls, v):
        if v == "auto":
            raise ValueError("Target language cannot be 'auto'")
        return v


class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str
    detected_language: Optional[str] = None


class Language(BaseModel):
    code: str
    name: str
