import asyncio
import tempfile
import os

import edge_tts
import cloudinary.uploader

from app.core import cloudinary_config  # noqa: F401
from app.db.database import SessionLocal
from app.crud.post import get_post
from app.crud.post_translation import get_post_translation_by_language, set_podcast_result
from app.models.post import PodcastStatus


VOICE_MAP = {
    "en": "en-US-AriaNeural",
    "tr": "tr-TR-EmelNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
}


async def _generate_audio_file(text: str, voice: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(output_path)


def process_podcast_generation(translation_id: int, post_id: int, language: str, post_version: int = 1):
    db = SessionLocal()
    tmp_path = None

    try:
        post = get_post(db, post_id)
        if post is None:
            return

        set_podcast_result(db, translation_id, PodcastStatus.processing)

        if language == post.language:
            text_to_speak = post.content
        else:
            translation = get_post_translation_by_language(db, post_id, language)
            if translation is None or translation.translated_content is None:
                set_podcast_result(db, translation_id, PodcastStatus.failed)
                return
            text_to_speak = translation.translated_content

        voice = VOICE_MAP.get(language, VOICE_MAP["en"])

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        asyncio.run(_generate_audio_file(text_to_speak, voice, tmp_path))

        upload_result = cloudinary.uploader.upload(
            tmp_path,
            folder="mediumvari/podcasts",
            resource_type="video",
        )

        audio_url = upload_result["secure_url"]

        set_podcast_result(
            db,
            translation_id,
            PodcastStatus.completed,
            audio_url=audio_url,
            source_version=post_version,
        )

    except Exception:
        set_podcast_result(db, translation_id, PodcastStatus.failed)

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        db.close()