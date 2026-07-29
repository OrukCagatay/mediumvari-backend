from fastapi import HTTPException, status
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
)

from app.crud.tag import (
    get_tag_by_name,
    create_tag
)

from app.crud.post_tag import create_post_tag

"""
def create_post_service(
    db: Session,
    post: PostCreate,           tag gelince burası değişti
    current_user: User
):              
    return create_post(db, post, current_user)
"""

def create_post_service(
    db: Session,
    post: PostCreate,
    current_user: User
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

    return db_post




def get_posts_service(
    db: Session,
    search: str | None,
    tag: str | None,
    topic_id: int | None,
    skip: int,
    limit: int,
    sort_by: PostSortBy,
):
    return get_posts(
    db,
    search,
    tag,
    topic_id,
    skip,
    limit,
    sort_by
    )


def get_post_service(
    db: Session,
    post_id: int
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return post


def update_post_service(
    db: Session,
    post_id: int,
    post_data: PostUpdate,
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

    return update_post(
        db,
        post,
        post_data
    )


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