from fastapi import APIRouter, Depends, status, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import current_user, optional_current_user

from fastapi import UploadFile, File
from app.services.post import upload_post_image_service

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
    delete_post_service,
    publish_post_service,
)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", response_model=PostResponse)
def create_new_post(
    post: PostCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return create_post_service(
        db,
        post,
        current_user,
        background_tasks,
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
    search: str | None = Query(default=None, description="Search posts by title"),
    skip: int = Query(default=0, ge=0, description="Number of posts to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum number of posts to return"),
    tag: str | None = Query(default=None, description="Filter posts by tag"),
    topic_id: int | None = Query(default=None, description="Filter posts by topic"),
    sort_by: PostSortBy = Query(default=PostSortBy.newest, description="Sort posts"),
    author_id: int | None = Query(default=None, description="Filter posts by author"),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(optional_current_user),
):
    return get_posts_service(
        db,
        search,
        tag,
        topic_id,
        skip,
        limit,
        sort_by,
        author_id,
        current_user,
    )


@router.get("/{post_id}", response_model=PostResponse)
def get_single_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(optional_current_user),
):
    return get_post_service(
        db,
        post_id,
        current_user,
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
        current_user,
    )


@router.patch("/{post_id}/publish", response_model=PostResponse)
def publish_post_route(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return publish_post_service(
        db,
        post_id,
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



@router.post("/{post_id}/image", response_model=PostResponse)
async def upload_post_image(
    post_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return await upload_post_image_service(db, post_id, current_user, file)