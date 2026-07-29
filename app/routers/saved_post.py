from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.auth import current_user

from app.models.user import User

from app.schemas.saved_post import SavedPostResponse
from app.schemas.post import PostResponse

from app.services.saved_post import (
    save_post_service,
    unsave_post_service,
    get_saved_posts_service
)

router = APIRouter(
    tags=["Saved Posts"]
)


@router.post(
    "/posts/{post_id}/save",
    response_model=SavedPostResponse
)
def save_post_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return save_post_service(
        db,
        current_user,
        post_id
    )



@router.delete(
    "/posts/{post_id}/save",
    response_model=SavedPostResponse
)
def unsave_post_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return unsave_post_service(
        db,
        current_user,
        post_id
    )



@router.get(
    "/me/saved",
    response_model=list[PostResponse]
)
def get_saved_posts_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return get_saved_posts_service(
        db,
        current_user
    )