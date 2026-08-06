import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.redis_client import redis_client
from app.models.post import Post, PostStatus
from app.models.like import Like

TRENDING_CACHE_KEY = "trending:daily"
TRENDING_LIMIT = 10
TRENDING_CACHE_TTL_SECONDS = 900  # 15 dakika


def compute_trending_posts(db: Session) -> list[int]:
    """Son 24 saatte en çok beğeni alan postların ID listesini hesaplar."""
    since = datetime.now(timezone.utc) - timedelta(hours=24)

    stmt = (
        select(Post.id, func.count(Like.user_id).label("like_count"))
        .join(Like, Like.post_id == Post.id)
        .where(Post.status == PostStatus.published)
        .where(Like.created_at >= since)
        .group_by(Post.id)
        .order_by(func.count(Like.user_id).desc())
        .limit(TRENDING_LIMIT)
    )

    results = db.execute(stmt).all()
    return [row.id for row in results]


def refresh_trending_cache(db: Session):
    """Trending listesini hesaplar ve Redis'e, TTL ile yazar."""
    post_ids = compute_trending_posts(db)
    redis_client.set(
        TRENDING_CACHE_KEY,
        json.dumps(post_ids),
        ex=TRENDING_CACHE_TTL_SECONDS,
    )


def get_cached_trending_ids() -> list[int] | None:
    """Redis'ten cache'lenmiş trending listesini okur. TTL dolmuşsa None döner."""
    cached = redis_client.get(TRENDING_CACHE_KEY)
    if cached is None:
        return None
    return json.loads(cached)