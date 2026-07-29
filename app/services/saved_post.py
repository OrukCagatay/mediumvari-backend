from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.crud.post import get_post
from app.crud.saved_post import (
    save_post,
    unsave_post,
    get_saved_post,
    get_saved_posts
)



def save_post_service(
    db: Session,
    current_user: User,
    post_id: int
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    saved_post = get_saved_post(
        db,
        current_user.id,
        post_id
    )

    if saved_post is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Post already saved."
        )

    save_post(
        db,
        current_user.id,
        post_id
    )

    return {
        "message": "Post saved successfully."
    }



def unsave_post_service(
    db: Session,
    current_user: User,
    post_id: int
):
    saved_post = get_saved_post(
        db,
        current_user.id,
        post_id
    )

    if saved_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved post not found."
        )

    unsave_post(
        db,
        saved_post
    )

    return {
        "message": "Post removed from saved posts."
    }


def get_saved_posts_service(
    db: Session,
    current_user: User
):
    return get_saved_posts(
        db,
        current_user.id
    )