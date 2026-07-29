from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.like import unlike_post,get_post_likes,count_likes

from app.crud.like import (
    like_post,
    get_like,
)

from app.crud.post import get_post


def like_post_service(
    db: Session,
    user_id: int,
    post_id: int
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    like = get_like(
        db,
        user_id,
        post_id
    )

    if like:
        raise HTTPException(
            status_code=409,
            detail="You already liked this post"
        )

    return like_post(
        db,
        user_id,
        post_id
    )


def unlike_post_service(
    db: Session,
    user_id: int,
    post_id: int
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    like = get_like(
        db,
        user_id,
        post_id
    )

    if like is None:
        raise HTTPException(
            status_code=404,
            detail="Like not found"
        )

    unlike_post(
        db,
        user_id,
        post_id
    )


def get_post_likes_service(
        db: Session,
        post_id:int
):

    post = get_post(db,post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
        
    return get_post_likes(db,post_id)


def count_likes_service(
    db: Session,
    post_id: int
):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return count_likes(
        db,
        post_id
    )
