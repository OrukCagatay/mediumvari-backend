from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import jwt

from datetime import datetime, timezone

from app.core.security import (
    create_access_token,
    create_refresh_token,
    password_hash
)

from app.schemas.auth import LoginRequest

from app.crud.blacklisted_token import blacklist_token,delete_expired_blacklisted_tokens

from app.schemas.user import UserCreate
from app.crud.user import (
    create_user,
    get_user_by_email,
)

from app.core.security import (
    decode_token,
    create_access_token
)

from sqlalchemy import select
from app.models.user import User




def register_user_service(
    db: Session,
    user: UserCreate
):
    try:
        return create_user(
            db,
            user
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu kullanıcı adı veya email zaten kullanılıyor."
        )



def login_user_service(
    db: Session,
    request: LoginRequest
):

    user = get_user_by_email(
        db,
        request.email
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not password_hash.verify(
        request.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value}
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(user.id),
            "role": user.role.value}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




def refresh_token_service(
    db: Session,
    refresh_token: str
):

    try:
        payload = decode_token(refresh_token)

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    stmt = select(User).where(
        User.id == int(user_id)
    )

    user = db.scalar(stmt)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }




def logout_user_service(
    db: Session,
    payload: dict,
):
    delete_expired_blacklisted_tokens(db)       # zamanı geçen tokeni her log outta sileriz 

    blacklist_token(
        db=db,
        jti=payload["jti"],
        expires_at=datetime.fromtimestamp(
            payload["exp"],
            tz=timezone.utc
        )
    )

    return {
        "message": "Successfully logged out."
    }