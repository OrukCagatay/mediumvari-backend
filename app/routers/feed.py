from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import current_user

from app.models.user import User

from app.schemas.post import (
    PostResponse,
    PostSortBy,
)

from app.services.feed import (
    get_following_feed_service,
    get_explore_feed_service,
)

router = APIRouter(tags=["Feed"])


@router.get(
    "/feed",
    response_model=list[PostResponse],
    summary="Browse your personalized feed",

    description="""
Returns posts created by users that the authenticated user follows.
"""
)
def get_following_feed_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user),
):
    return get_following_feed_service(
        db,
        current_user,
    )


@router.get(
    "/explore",
    response_model=list[PostResponse],
    summary="Browse the explore feed",
    description="""
Returns a paginated list of public posts.

Supports searching, filtering by topic or tag, and sorting results.
"""
)
def get_explore_feed_route(
    search: str | None = Query(
        default=None,
        description="Search posts by title"
    ),
    tag: str | None = Query(
        default=None,
        description="Filter posts by tag"
    ),
    topic_id: int | None = Query(
        default=None,
        description="Filter posts by topic"
    ),
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of posts to skip"
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of posts to return"
    ),
    sort_by: PostSortBy = Query(
        default=PostSortBy.newest,
        description="Sort posts"
    ),
    db: Session = Depends(get_db),
):
    return get_explore_feed_service(
        db=db,
        search=search,
        tag=tag,
        topic_id=topic_id,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
    )