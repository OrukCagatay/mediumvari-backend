from fastapi import HTTPException, status, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate
from app.schemas.post import PostSortBy

from app.crud.post import (
    create_post,
    get_posts,
    get_post,
    update_post,
    delete_post,
    publish_post,
)

from app.crud.tag import (
    get_tag_by_name,
    create_tag
)

from app.crud.post_tag import create_post_tag

from app.crud.post_translation import (
    get_post_translation_by_language,
    create_pending_translation,
    create_completed_translation_for_own_language,
)

from app.services.image_upload import upload_image_to_cloudinary
from app.services.translation_generation import process_translation_generation
from app.services.podcast_generation import process_podcast_generation


MIN_PODCAST_WORDS = 300


def _trigger_translations_and_podcasts(
    db: Session,
    post,
    translation_languages: list[str],
    podcast_languages: list[str],
    background_tasks: BackgroundTasks,
):
    translation_languages = [
        lang for lang in set(translation_languages) if lang != post.language
    ]
    podcast_languages = list(set(podcast_languages))

    translation_records = {}
    for lang in translation_languages:
        existing = get_post_translation_by_language(db, post.id, lang)
        record = existing or create_pending_translation(db, post.id, lang, source_version=post.version)
        translation_records[lang] = record
        if existing is None:
            background_tasks.add_task(process_translation_generation, record.id, post.id, lang, post.version)

    for lang in podcast_languages:
        if lang == post.language:
            word_count = len(post.content.split())
            if word_count < MIN_PODCAST_WORDS:
                continue  # sessizce atla — frontend zaten bunu engellemiş olmalı

            existing = get_post_translation_by_language(db, post.id, lang)
            record = existing or create_completed_translation_for_own_language(db, post.id, lang, source_version=post.version)
            if existing is None or existing.podcast_status.value == "none":
                background_tasks.add_task(process_podcast_generation, record.id, post.id, lang, post.version)
        else:
            record = translation_records.get(lang)
            if record is None:
                record = get_post_translation_by_language(db, post.id, lang)
                if record is None:
                    record = create_pending_translation(db, post.id, lang, source_version=post.version)
                    background_tasks.add_task(process_translation_generation, record.id, post.id, lang, post.version)

            background_tasks.add_task(
                _translate_then_podcast, record.id, post.id, lang, post.version
            )


def _translate_then_podcast(translation_id: int, post_id: int, language: str, post_version: int):
    process_translation_generation(translation_id, post_id, language, post_version)

    from app.db.database import SessionLocal
    from app.crud.post_translation import get_post_translation_by_language
    from app.models.post_translation import TranslationStatus

    db = SessionLocal()
    try:
        translation = get_post_translation_by_language(db, post_id, language)
        if translation and translation.translation_status == TranslationStatus.completed:
            word_count = len((translation.translated_content or "").split())
            if word_count >= MIN_PODCAST_WORDS:
                process_podcast_generation(translation_id, post_id, language, post_version)
    finally:
        db.close()


def create_post_service(
    db: Session,
    post: PostCreate,
    current_user: User,
    background_tasks: BackgroundTasks,
):
    db_post = create_post(
        db,
        post,
        current_user
    )

    for tag_name in post.tags:

        tag = get_tag_by_name(
            db,
            tag_name
        )

        if tag is None:
            tag = create_tag(
                db,
                tag_name
            )

        create_post_tag(
            db,
            db_post.id,
            tag.id
        )

    _trigger_translations_and_podcasts(
        db, db_post, post.translation_languages, post.podcast_languages, background_tasks
    )

    return db_post


def get_posts_service(
    db: Session,
    search: str | None,
    tag: str | None,
    topic_id: int | None,
    skip: int,
    limit: int,
    sort_by: PostSortBy,
    author_id: int | None = None,
    current_user: User | None = None,
):
    include_drafts = bool(
        current_user and author_id and current_user.id == author_id
    )

    return get_posts(
        db,
        search,
        tag,
        topic_id,
        skip,
        limit,
        sort_by,
        author_id,
        include_drafts,
    )


def get_post_service(
    db: Session,
    post_id: int,
    current_user: User | None = None,
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.status.value == "draft":
        if current_user is None or current_user.id != post.author_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

    return post


def update_post_service(
    db: Session,
    post_id: int,
    post_data: PostUpdate,
    current_user: User,
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    updated_post = update_post(
        db,
        post,
        post_data
    )

    return updated_post


def publish_post_service(
    db: Session,
    post_id: int,
    current_user: User
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    return publish_post(db, post)


def delete_post_service(
    db: Session,
    post_id: int,
    current_user: User
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    delete_post(
        db,
        post
    )


async def upload_post_image_service(
    db: Session,
    post_id: int,
    current_user: User,
    file: UploadFile,
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    image_url = await upload_image_to_cloudinary(file)

    post.cover_image_url = image_url
    db.commit()
    db.refresh(post)

    return post