from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.admin import admin_authenticator

from app.models.user import User

from app.schemas.user import UserResponse
from app.schemas.admin import (
    DashboardResponse,
    UserRoleUpdate,
)

from app.services.admin import (
    get_all_users_service,
    get_user_service,
    update_user_role_service,
    delete_user_service,
    get_dashboard_service,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get(
    "/dashboard",
    response_model=DashboardResponse,
    summary="Get dashboard statistics",
    description="""
Returns statistics about the application.

Admin only.
"""
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),
):
    return get_dashboard_service(db)


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Get all users",
    description="""
Returns all registered users.

Admin only.
"""
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),
):
    return get_all_users_service(db)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="""
Returns a single user.

Admin only.
""",
    responses={
        404: {
            "description": "User not found"
        }
    }
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),
):
    return get_user_service(
        db,
        user_id,
    )


@router.patch(
    "/users/{user_id}/role",
    response_model=UserResponse,
    summary="Update user role",
    description="""
Updates the role of a user.

Admin only.
""",
    responses={
        404: {
            "description": "User not found"
        }
    }
)
def update_user_role(
    user_id: int,
    request: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),
):
    return update_user_role_service(
        db,
        user_id,
        request.role,
    )


@router.delete(
    "/users/{user_id}",
    summary="Delete user",
    description="""
Deletes a user and all related data.

Admin only.
""",
    responses={
        404: {
            "description": "User not found"
        }
    }
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),  # bunu kullanmıyoeuz ama dependency çalışsın amaç o yoksa return
):                                                 #falan etmiyoruz bunu admin mi check etsin diye
    return delete_user_service(
        db,
        user_id,
    )