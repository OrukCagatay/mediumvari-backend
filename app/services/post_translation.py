from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.post_translation import TranslationStatus
from app.models.post import PodcastStatus

from app.crud.post import get_post
from app.crud.post_translation import (
    get_post_translations,
    get_post_translation_by_language,
    create_pending_translation,
)

from app.services.translation_generation import process_translation_generation
from app.services.podcast_generation import process_podcast_generation


ALLOWED_LANGUAGES = {"en", "tr", "fr", "de"}
MIN_PODCAST_WORDS = 300


def get_post_translations_service(
    db: Session,
    post_id: int,
    current_user: User | None,
):
    post = get_post(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    translations = get_post_translations(db, post_id)

    for t in translations:
        # Outdated podcast ses dosyası, hiçbir kullanıcıya (sahibi hariç ayrı bir
        # mekanizmada yönetilir) dinletilmez — dosya Cloudinary'de durur ama URL gizlenir.
        if t.podcast_status == PodcastStatus.outdated:
            t.audio_url = None

    if current_user is None:
        for t in translations:
            t.audio_url = None
            t.podcast_status = PodcastStatus.none

    return translations


def request_translation_service(
    db: Session,
    post_id: int,
    language: str,
    current_user: User,
    background_tasks: BackgroundTasks,
):
    if language not in ALLOWED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language. Choose one of: {', '.join(ALLOWED_LANGUAGES)}"
        )

    post = get_post(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the post owner can request a new translation"
        )

    if language == post.language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This post is already in the requested language"
        )

    existing = get_post_translation_by_language(db, post_id, language)

    if existing is not None:
        if existing.translation_status == TranslationStatus.processing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Translation is already in progress"
            )
        # completed ise ve GÜNCEL versiyona aitse, tekrar üretmeye gerek yok.
        # outdated ise, yeniden üretime izin veriyoruz (aşağıya devam eder).
        if existing.translation_status == TranslationStatus.completed:
            return existing

    translation = existing or create_pending_translation(db, post_id, language, source_version=post.version)

    background_tasks.add_task(process_translation_generation, translation.id, post_id, language, post.version)

    return translation


def request_podcast_service(
    db: Session,
    post_id: int,
    language: str,
    current_user: User,
    background_tasks: BackgroundTasks,
):
    if language not in ALLOWED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language. Choose one of: {', '.join(ALLOWED_LANGUAGES)}"
        )

    post = get_post(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the post owner can request a new podcast"
        )

    if post.status.value == "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot generate a podcast for a draft post"
        )

    existing = get_post_translation_by_language(db, post_id, language)

    # Metin kaynağını belirle (kelime sayısı kontrolü için)
    if language == post.language:
        text_to_check = post.content
    else:
        if existing is None or existing.translation_status not in (
            TranslationStatus.completed, TranslationStatus.outdated
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This post must be translated to this language before generating a podcast. "
                       "Call POST /posts/{post_id}/translate first."
            )
        text_to_check = existing.translated_content or ""

    word_count = len(text_to_check.split())
    if word_count < MIN_PODCAST_WORDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post must be at least {MIN_PODCAST_WORDS} words for a podcast (currently {word_count})"
        )

    if existing is not None:
        if existing.podcast_status == PodcastStatus.processing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Podcast generation is already in progress"
            )
        if existing.podcast_status == PodcastStatus.completed:
            return existing

    translation = existing or create_pending_translation(db, post_id, language, source_version=post.version)

    background_tasks.add_task(process_podcast_generation, translation.id, post_id, language, post.version)

    return translation