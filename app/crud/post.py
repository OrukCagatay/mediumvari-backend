from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.post import Post, PostStatus
from app.models.user import User
from app.models.like import Like
from app.models.tag import Tag
from app.models.post_tag import PostTag

from app.schemas.post import PostCreate, PostUpdate, PostSortBy
from sqlalchemy import select, or_, func

from app.services.language_detection import detect_language
from app.crud.post_translation import mark_all_outdated


def normalize_text(text: str) -> str:
    """Boşluk/satır sonu farklarını göz ardı ederek metni karşılaştırılabilir hale getirir."""
    return " ".join(text.split())


def create_post(
    db: Session,
    post: PostCreate,
    current_user: User
):
    detected_language = detect_language(post.content)

    db_post = Post(
        title=post.title,
        content=post.content,
        author_id=current_user.id,
        topic_id=post.topic_id,
        status=post.status,
        cover_image_url=post.cover_image_url,
        language=detected_language,
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_posts(
    db: Session,
    search: str | None,
    tag: str | None,
    topic_id: int | None,
    skip: int,
    limit: int,
    sort_by: PostSortBy = PostSortBy.newest,
    author_id: int | None = None,
    include_drafts: bool = False,
):

    stmt = select(Post).options(
        selectinload(Post.author),
        selectinload(Post.topic),
    )

    if not include_drafts:
        stmt = stmt.where(Post.status == PostStatus.published)

    if search:
        stmt = stmt.where(
            or_(
                Post.title.ilike(f"%{search}%"),
                Post.content.ilike(f"%{search}%")
            )
        )

    if topic_id:
        stmt = stmt.where(
            Post.topic_id == topic_id
        )

    if author_id:
        stmt = stmt.where(
            Post.author_id == author_id
        )

    if tag:
        stmt = (
            stmt.join(PostTag)
            .join(Tag)
            .where(Tag.name == tag)
        )

    if sort_by == PostSortBy.newest:
        stmt = stmt.order_by(Post.created_at.desc())

    elif sort_by == PostSortBy.oldest:
        stmt = stmt.order_by(Post.created_at.asc())

    elif sort_by == PostSortBy.most_liked:
        stmt = (
            stmt.outerjoin(Like)
            .group_by(Post.id)
            .order_by(func.count(Like.user_id).desc())
        )

    stmt = stmt.offset(skip).limit(limit)

    return db.scalars(stmt).all()


def get_post(
    db: Session,
    post_id: int
):
    stmt = (
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.topic),
        )
        .where(Post.id == post_id)
    )
    return db.scalar(stmt)


def update_post(
    db: Session,
    post: Post,
    post_data: PostUpdate
):
    content_changed = normalize_text(post.content) != normalize_text(post_data.content)

    post.title = post_data.title
    post.content = post_data.content
    post.topic_id = post_data.topic_id
    post.cover_image_url = post_data.cover_image_url

    if content_changed:
        post.version += 1

    db.commit()
    db.refresh(post)

    if content_changed:
        mark_all_outdated(db, post.id)

    return post


def publish_post(
    db: Session,
    post: Post
):
    post.status = PostStatus.published
    db.commit()
    db.refresh(post)
    return post


def delete_post(
    db: Session,
    post: Post
):
    db.delete(post)
    db.commit()