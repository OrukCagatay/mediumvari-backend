from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.auth import current_user

from app.models.user import User

from app.schemas.follow import FollowResponse,FollowCountResponse
from app.schemas.user import UserPreview

from app.services.follow import (
    follow_user_service,
    unfollow_user_service,
    get_followers_service,
    get_following_service,
    followers_count_service,
    following_count_service
)

router = APIRouter(
    prefix="/users",
    tags=["Follows"]
)


@router.post(
    "/{user_id}/follow",
    response_model=FollowResponse
)
def follow_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return follow_user_service(
        db,
        current_user,
        user_id
    )



@router.delete(
    "/{user_id}/follow",
    response_model=FollowResponse
)
def unfollow_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return unfollow_user_service(
        db,
        current_user,
        user_id
    )


@router.get(
    "/{user_id}/followers",
    response_model=list[UserPreview]
)
def get_followers_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_followers_service(
        db,
        user_id
    )


@router.get(
    "/{user_id}/following",
    response_model=list[UserPreview]
)
def get_following_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_following_service(
        db,
        user_id
    )


@router.get(
    "/{user_id}/followers/count",
    response_model=FollowCountResponse
)
def followers_count_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    return {
        "count": followers_count_service(
            db,
            user_id
        )
    }



@router.get(
    "/{user_id}/following/count",
    response_model=FollowCountResponse
)
def following_count_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    return {
        "count": following_count_service(
            db,
            user_id
        )
    }