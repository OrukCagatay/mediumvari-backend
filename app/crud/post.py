from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.user import User
from app.models.like import Like
from app.models.tag import Tag
from app.models.post_tag import PostTag

from app.schemas.post import PostCreate, PostUpdate,PostSortBy
from sqlalchemy import select, or_,func


def create_post(
    db: Session,
    post: PostCreate,
    current_user: User
):
    db_post = Post(
        title=post.title,
        content=post.content,
        author_id=current_user.id,
        topic_id=post.topic_id
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
):

    stmt = select(Post)

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
                                                ## sort için şemada enum ve like ile join ettik
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
    stmt = select(Post).where(Post.id == post_id)
    return db.scalar(stmt)


def update_post(
    db: Session,
    post: Post,
    post_data: PostUpdate
):
    post.title = post_data.title
    post.content = post_data.content
    post.topic_id = post_data.topic_id

    db.commit()
    db.refresh(post)

    return post


def delete_post(
    db: Session,
    post: Post
):
    db.delete(post)
    db.commit()