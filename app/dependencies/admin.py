from fastapi import Depends, HTTPException, status

from app.dependencies.auth import current_user
from app.models.user import User, UserRole


class AdminAuthenticator:

    def __call__(
        self,
        current_user: User = Depends(current_user)
    ) -> User:

        if current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required."
            )

        return current_user


admin_authenticator = AdminAuthenticator()