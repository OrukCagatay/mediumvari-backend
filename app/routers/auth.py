from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth import (
    register_user_service,
    login_user_service,
    refresh_token_service
)

from app.schemas.user import RefreshTokenRequest
from app.schemas.auth import LoginRequest

from app.dependencies.current_payload import current_payload
from app.services.auth import logout_user_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse,summary="Register a new user",
    description="""
Creates a new user account.

Email addresses must be unique.
""",
    responses={
    409: {
        "description": "Email already exists"
    }
})
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user_service(
        db,
        user
    )


@router.post("/login", response_model=Token,summary="Authenticate user",
    description="""
Authenticates the user and returns an access token and refresh token.
""",
    responses={
    401: {
        "description": "Invalid email or password"
    }
})
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    return login_user_service(
        db,
        request
    )


@router.post("/refresh",summary="Refresh access token",
    description="""
Generates a new access token using a valid refresh token.
""",
    responses={
    401: {
        "description": "Invalid or expired refresh token"
    }
})
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_token_service(
        db,
        request.refresh_token
    )



@router.post(
    "/logout",
    summary="Logout user",
    description="""
Revokes the current access token by adding it to the blacklist.
"""
)
def logout(
    payload: dict = Depends(current_payload),
    db: Session = Depends(get_db),
):
    return logout_user_service(
        db=db,
        payload=payload,
    )