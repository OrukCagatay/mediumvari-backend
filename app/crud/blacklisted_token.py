from sqlalchemy.orm import Session
from sqlalchemy import select

from sqlalchemy import delete
from datetime import datetime, timezone


from app.models.blacklisted_token import BlacklistedToken


def blacklist_token(
    db: Session,
    jti: str,
    expires_at,
):
    token = BlacklistedToken(
        jti=jti,
        expires_at=expires_at,
    )

    db.add(token)
    db.commit()

    return token


def is_token_blacklisted(
    db: Session,
    jti: str,
) -> bool:

    stmt = (
        select(BlacklistedToken)
        .where(BlacklistedToken.jti == jti)
    )

    token = db.scalar(stmt)

    return token is not None



def delete_expired_blacklisted_tokens(
    db: Session,
):
    stmt = delete(blacklist_token).where(
        blacklist_token.expires_at <
        datetime.now(timezone.utc)
    )

    db.execute(stmt)
    db.commit()