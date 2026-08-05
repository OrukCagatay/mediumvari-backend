from datetime import datetime
from pydantic import BaseModel

from app.models.post_translation import TranslationStatus
from app.models.post import PodcastStatus


class PostTranslationResponse(BaseModel):
    id: int
    language: str
    translated_title: str | None
    translated_content: str | None
    translation_status: TranslationStatus
    audio_url: str | None
    podcast_status: PodcastStatus
    source_version: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }