from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.comment import (
    create_comment,
    get_comment,
    get_post_comments,
    update_comment,
    delete_comment
)

from app.crud.post import get_post

from app.models.user import User
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate
)


def create_comment_service(
    db: Session,
    comment: CommentCreate,
    current_user: User,
    post_id: int
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.status.value == "draft":
        raise HTTPException(
            status_code=400,
            detail="Cannot comment on a draft post"
        )

    return create_comment(
        db,
        comment.content,
        current_user.id,
        post_id
    )


def get_post_comments_service(
    db: Session,
    post_id: int
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return get_post_comments(
        db,
        post_id
    )


def update_comment_service(
    db: Session,
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User
):
    comment = get_comment(
        db,
        comment_id
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return update_comment(
        db,
        comment,
        comment_data.content
    )


def delete_comment_service(
    db: Session,
    comment_id: int,
    current_user: User
):
    comment = get_comment(
        db,
        comment_id
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    delete_comment(
        db,
        comment
    )