from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import current_user, optional_current_user
from app.models.user import User

from app.schemas.post_translation import PostTranslationResponse

from app.services.post_translation import (
    get_post_translations_service,
    request_translation_service,
    request_podcast_service,
)

router = APIRouter(
    prefix="/posts",
    tags=["Translations & Podcasts"]
)


@router.get(
    "/{post_id}/translations",
    response_model=list[PostTranslationResponse],
    summary="List translations and podcasts for this post",
    description="""
Returns all available translations for this post.

Publicly accessible — anyone can read translated text.
Podcast audio is only included if the requester is logged in.
"""
)
def get_post_translations_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(optional_current_user),
):
    return get_post_translations_service(db, post_id, current_user)


@router.post(
    "/{post_id}/translate",
    response_model=PostTranslationResponse,
    status_code=202,
    summary="Translate this post to another language",
    description="Owner only. Starts translating the post's text in the background."
)
def request_translation_route(
    post_id: int,
    background_tasks: BackgroundTasks,
    language: str = Query(..., description="en, tr, fr, or de"),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return request_translation_service(db, post_id, language, current_user, background_tasks)


@router.post(
    "/{post_id}/podcast",
    response_model=PostTranslationResponse,
    status_code=202,
    summary="Generate a podcast for this post",
    description="""
Owner only. Login required to generate.

If the language is not the post's own language, it must already be translated
(via POST /posts/{post_id}/translate) before a podcast can be generated.
"""
)
def request_podcast_route(
    post_id: int,
    background_tasks: BackgroundTasks,
    language: str = Query(..., description="en, tr, fr, or de"),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return request_podcast_service(db, post_id, language, current_user, background_tasks)