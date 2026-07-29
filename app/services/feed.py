from sqlalchemy.orm import Session

from app.crud.feed import get_following_feed
from app.crud.post import get_posts

from app.models.user import User

from app.schemas.post import PostSortBy


def get_following_feed_service(
    db: Session,
    current_user: User,
):
    return get_following_feed(
        db,
        current_user.id,
    )


def get_explore_feed_service(
    db: Session,
    search: str | None,
    tag: str |None,
    topic_id: int | None,
    skip: int,
    limit: int,
    sort_by: PostSortBy,
):
    return get_posts(
        db=db,
        search=search,
        tag=tag,
        topic_id=topic_id,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
    )