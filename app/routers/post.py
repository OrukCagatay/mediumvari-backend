from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import current_user

from app.models.user import User

from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostSortBy
)

from app.services.post import (
    create_post_service,
    get_posts_service,
    get_post_service,
    update_post_service,
    delete_post_service
)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", response_model=PostResponse)
def create_new_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return create_post_service(
        db,
        post,
        current_user
    )


@router.get(
    "/",
    response_model=list[PostResponse],
    summary="Browse posts",
    description="""
Returns a paginated list of posts.

Supports searching, filtering by topic or tag, and sorting results.
"""
)
def get_all_posts(
    search: str | None = Query(
        default=None,
        description="Search posts by title"
    ),
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of posts to skip"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of posts to return"
    ),
    tag: str | None = Query(
        default=None,
        description="Filter posts by tag"
    ),
    topic_id: int | None = Query(
        default=None,
        description="Filter posts by topic"
    ),
    sort_by: PostSortBy = Query(
        default=PostSortBy.newest,
        description="Sort posts"
    ),
    db: Session = Depends(get_db),
):
    return get_posts_service(
        db,
        search,
        tag,
        skip,
        topic_id,
        limit,
        sort_by
    )

@router.get("/{post_id}", response_model=PostResponse)
def get_single_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    return get_post_service(
        db,
        post_id
    )


@router.put("/{post_id}", response_model=PostResponse)
def update_post_route(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return update_post_service(
        db,
        post_id,
        post_data,
        current_user
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    delete_post_service(
        db,
        post_id,
        current_user
    )