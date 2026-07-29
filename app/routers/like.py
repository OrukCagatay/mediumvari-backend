from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.auth import current_user
from app.models.user import User

from app.schemas.user import UserPreview

from app.services.like import get_post_likes_service
from app.services.like import (
    like_post_service,
    unlike_post_service,
    count_likes_service
)

router = APIRouter(
    prefix="/posts",
    tags=["Likes"]
)


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
def like_post_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return like_post_service(
        db,
        current_user.id,
        post_id
    )


@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    unlike_post_service(
        db,
        current_user.id,
        post_id
    )


@router.get("/{post_id}/likes", response_model=list[UserPreview])
def get_post_likes_route(
    post_id: int,
    db: Session = Depends(get_db)
):
    return get_post_likes_service(
        db,
        post_id
    )


@router.get("/{post_id}/likes/count")
def count_likes_route(
    post_id: int,
    db: Session = Depends(get_db)
):
    return {
        "likes_count": count_likes_service(
            db,
            post_id
        )
    }