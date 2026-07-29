from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.auth import current_user

from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse
)

from app.services.comment import (
    create_comment_service,
    get_post_comments_service,
    update_comment_service,
    delete_comment_service
)

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/posts/{post_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment_route(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return create_comment_service(
        db,
        comment,
        current_user,
        post_id
    )


@router.get(
    "/posts/{post_id}",
    response_model=list[CommentResponse]
)
def get_post_comments_route(
    post_id: int,
    db: Session = Depends(get_db)
):
    return get_post_comments_service(
        db,
        post_id
    )


@router.put(
    "/{comment_id}",
    response_model=CommentResponse
)
def update_comment_route(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return update_comment_service(
        db,
        comment_id,
        comment_data,
        current_user
    )


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment_route(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    delete_comment_service(
        db,
        comment_id,
        current_user
    )