from app.db.database import SessionLocal
from app.crud.post import get_post
from app.crud.post_translation import set_translation_result
from app.models.post_translation import TranslationStatus
from app.services.translation import translate_post_content, TranslationError


def process_translation_generation(translation_id: int, post_id: int, target_language: str, post_version: int = 1):
    db = SessionLocal()

    try:
        post = get_post(db, post_id)
        if post is None:
            return

        set_translation_result(db, translation_id, TranslationStatus.processing)

        translated_title, translated_content = translate_post_content(
            title=post.title,
            content=post.content,
            source_language=post.language,
            target_language=target_language,
        )

        set_translation_result(
            db,
            translation_id,
            TranslationStatus.completed,
            translated_title=translated_title,
            translated_content=translated_content,
            source_version=post_version,
        )

    except TranslationError as e:
        print(f"[TRANSLATION] TranslationError: {e}")
        set_translation_result(db, translation_id, TranslationStatus.failed)

    except Exception as e:
        print(f"[TRANSLATION] Unexpected error: {type(e).__name__}: {e}")
        set_translation_result(db, translation_id, TranslationStatus.failed)

    finally:
        db.close()