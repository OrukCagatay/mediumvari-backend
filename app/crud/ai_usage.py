from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.ai_usage import AIUsage


def count_requests_today(db: Session, user_id: int) -> int:
    since = datetime.now(timezone.utc) - timedelta(hours=24)

    stmt = select(func.count()).where(
        AIUsage.user_id == user_id,
        AIUsage.created_at >= since
    )

    return db.scalar(stmt)


def log_usage(db: Session, user_id: int):
    usage = AIUsage(user_id=user_id)
    db.add(usage)
    db.commit()