from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from sqlalchemy import select

import jwt

from app.crud.blacklisted_token import is_token_blacklisted

from app.db.database import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM


# Swagger'a "Bearer Authentication" kullandığımızı söyler.
# Authentication işlemini yapmaz, sadece dokümantasyon ve token girişini sağlar.
security = HTTPBearer(auto_error=False)


class CurrentUser:

    def get_authorization_header(
        self,
        request: Request
    ) -> str:

        authorization = request.headers.get("Authorization")

        if authorization is None:
            raise HTTPException(
                status_code=401,
                detail="Authorization header is missing"
            )

        return authorization


    def extract_token(
        self,
        authorization: str
    ) -> str:

        parts = authorization.split()

        if len(parts) != 2:
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization header"
            )

        scheme, token = parts

        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )

        return token


    def decode_token(
        self,
        token: str
    ) -> dict:

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            return payload

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )



    def check_blacklist(
        self,
        payload: dict,
        db: Session,
    ):

        jti = payload.get("jti")

        if jti is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        if is_token_blacklisted(db, jti):
            raise HTTPException(
                status_code=401,
                detail="Token has been revoked"
            )

    


    def get_user(
        self,
        payload: dict,
        db: Session
    ) -> User:

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
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

        return user


    def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials | None = Depends(security),
        db: Session = Depends(get_db)
    ):

        # Swagger'dan geldiyse
        if credentials is not None:
            authorization = (
                f"{credentials.scheme} {credentials.credentials}"
            )

        # Normal HTTP isteğinden geldiyse
        else:
            authorization = self.get_authorization_header(request)

        token = self.extract_token(authorization)

        payload = self.decode_token(token)

        self.check_blacklist(
            payload,
            db
        )

        user = self.get_user(
            payload,
            db
        )

        return user


current_user = CurrentUser()