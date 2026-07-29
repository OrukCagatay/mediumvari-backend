from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.follow import (
    follow_user,
    unfollow_user,
    get_follow,
    get_followers,
    get_following,
    followers_count,
    following_count
)

from app.crud.user import get_user

from app.models.user import User

from app.schemas.follow import FollowResponse



def follow_user_service(
    db: Session,
    current_user: User,
    user_id: int
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself."
        )

    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    follow = get_follow(
        db,
        current_user.id,
        user_id
    )

    if follow is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already follow this user."
        )

    follow_user(
        db,
        current_user.id,
        user_id
    )

    return {
        "message": "User followed successfully."
    }



def unfollow_user_service(
    db: Session,
    current_user: User,
    user_id: int
):
    follow = get_follow(
        db,
        current_user.id,
        user_id
    )

    if follow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow relationship not found."
        )

    unfollow_user(
        db,
        follow
    )

    return {
        "message": "User unfollowed successfully."
    }




def get_followers_service(
    db: Session,
    user_id: int
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return get_followers(
        db,
        user_id
    )



def get_following_service(
    db: Session,
    user_id: int
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return get_following(
        db,
        user_id
    )



def followers_count_service(
    db: Session,
    user_id: int
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return followers_count(
        db,
        user_id
    )


def following_count_service(
    db: Session,
    user_id: int
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return following_count(
        db,
        user_id
    )