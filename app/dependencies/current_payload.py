from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import decode_token

security = HTTPBearer(auto_error=False)


class CurrentPayload:

    def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials | None = Depends(security),
    ) -> dict:

        if credentials is not None:
            authorization = (
                f"{credentials.scheme} {credentials.credentials}"
            )
        else:
            authorization = request.headers.get("Authorization")

        if authorization is None:
            raise HTTPException(
                status_code=401,
                detail="Authorization header is missing"
            )

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

        return decode_token(token)


current_payload = CurrentPayload()