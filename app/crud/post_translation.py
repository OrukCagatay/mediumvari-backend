from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post_translation import PostTranslation, TranslationStatus
from app.models.post import PodcastStatus


def get_post_translations(
    db: Session,
    post_id: int
):
    stmt = select(PostTranslation).where(PostTranslation.post_id == post_id)
    return db.scalars(stmt).all()


def get_post_translation_by_language(
    db: Session,
    post_id: int,
    language: str
):
    stmt = select(PostTranslation).where(
        PostTranslation.post_id == post_id,
        PostTranslation.language == language,
    )
    return db.scalar(stmt)


def create_pending_translation(
    db: Session,
    post_id: int,
    language: str,
    source_version: int = 1,
):
    translation = PostTranslation(
        post_id=post_id,
        language=language,
        translation_status=TranslationStatus.pending,
        source_version=source_version,
    )

    db.add(translation)
    db.commit()
    db.refresh(translation)

    return translation


def set_translation_result(
    db: Session,
    translation_id: int,
    status: TranslationStatus,
    translated_title: str | None = None,
    translated_content: str | None = None,
    source_version: int | None = None,
):
    translation = db.get(PostTranslation, translation_id)

    if translation is None:
        return None

    translation.translation_status = status

    if translated_title is not None:
        translation.translated_title = translated_title

    if translated_content is not None:
        translation.translated_content = translated_content

    if source_version is not None:
        translation.source_version = source_version

    db.commit()
    db.refresh(translation)

    return translation


def set_podcast_result(
    db: Session,
    translation_id: int,
    status: PodcastStatus,
    audio_url: str | None = None,
    source_version: int | None = None,
):
    translation = db.get(PostTranslation, translation_id)

    if translation is None:
        return None

    translation.podcast_status = status

    if audio_url is not None:
        translation.audio_url = audio_url

    if source_version is not None:
        translation.source_version = source_version

    db.commit()
    db.refresh(translation)

    return translation


def create_completed_translation_for_own_language(
    db: Session,
    post_id: int,
    language: str,
    source_version: int = 1,
):
    """Postun kendi dili için bir kayıt oluşturur — çeviri gerekmediği için
    translation_status baştan 'completed' olarak işaretlenir."""
    translation = PostTranslation(
        post_id=post_id,
        language=language,
        translation_status=TranslationStatus.completed,
        source_version=source_version,
    )
    db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation


def mark_all_outdated(
    db: Session,
    post_id: int,
):
    """Bir postun content'i değiştiğinde, o posta ait TÜM çeviri ve podcast
    kayıtlarını 'outdated' olarak işaretler. Veriler silinmez, sadece durum değişir."""
    translations = get_post_translations(db, post_id)

    for t in translations:
        if t.translation_status == TranslationStatus.completed:
            t.translation_status = TranslationStatus.outdated
        if t.podcast_status == PodcastStatus.completed:
            t.podcast_status = PodcastStatus.outdated

    db.commit()

    return translations