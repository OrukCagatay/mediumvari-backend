from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.admin import (
    get_all_users,
    get_user_by_id,
    update_user_role,
    delete_user,
    get_dashboard_stats,
)

from app.crud.post import get_post
from app.crud.comment import get_comment
from app.crud.admin import admin_delete_post, admin_delete_comment

from app.models.user import UserRole

from app.schemas.admin import DashboardResponse


def get_all_users_service(
    db: Session,
):
    return get_all_users(db)


def get_user_service(
    db: Session,
    user_id: int,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


def update_user_role_service(
    db: Session,
    user_id: int,
    role: UserRole,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return update_user_role(
        db,
        user,
        role,
    )


def admin_delete_post_service(db: Session, post_id: int):
    post = get_post(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    admin_delete_post(db, post)

    return {"message": "Post deleted successfully"}



def admin_delete_comment_service(db: Session, comment_id: int):
    comment = get_comment(db, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    admin_delete_comment(db, comment)

    return {"message": "Comment deleted successfully"}


def delete_user_service(
    db: Session,
    user_id: int,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    delete_user(
        db,
        user,
    )

    return {
        "message": "User deleted successfully"
    }


def get_dashboard_service(
    db: Session,
) -> DashboardResponse:

    stats = get_dashboard_stats(db)

    return DashboardResponse(
        total_users=stats["total_users"],
        total_posts=stats["total_posts"],
        total_comments=stats["total_comments"],
        total_likes=stats["total_likes"],
    )