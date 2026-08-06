from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.post import PostResponse
from app.services.trending import get_cached_trending_ids, refresh_trending_cache
from app.crud.post import get_posts_by_ids_ordered

router = APIRouter(
    prefix="/posts",
    tags=["Trending"]
)


@router.get(
    "/trending",
    response_model=list[PostResponse],
    summary="Get today's trending posts",
    description="Returns the top 10 most-liked posts from the last 24 hours, cached in Redis and refreshed hourly."
)
def get_trending_posts(db: Session = Depends(get_db)):
    post_ids = get_cached_trending_ids()

    if post_ids is None:
        # Cache boşsa (örn. uygulama yeni başladıysa), anlık hesapla
        refresh_trending_cache(db)
        post_ids = get_cached_trending_ids() or []

    return get_posts_by_ids_ordered(db, post_ids)