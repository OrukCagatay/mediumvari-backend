from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import jwt
import uuid

password_hash = PasswordHash.recommended()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
)


def create_token(
    data: dict,
    expires_delta: timedelta
):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({
        "exp": expire,
        "jti": str(uuid.uuid4())
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_access_token(
    data: dict
):
    return create_token(
        data,
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


def create_refresh_token(
    data: dict
):
    return create_token(
        data,
        timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )


def decode_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )