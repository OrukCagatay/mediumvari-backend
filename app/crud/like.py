from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func

from app.models.like import Like
from app.models.user import User
from app.models.post import Post


def like_post(
    db: Session,
    user_id: int,
    post_id: int
):
    db_like = Like(
        user_id=user_id,
        post_id=post_id
    )

    db.add(db_like)
    db.commit()
    db.refresh(db_like)

    return db_like


def unlike_post(
    db: Session,
    user_id: int,
    post_id: int
):
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.post_id == post_id
    )
    like = db.scalar(stmt)

    db.delete(like)
    db.commit()


def get_like(
    db: Session,
    user_id: int,
    post_id: int
):
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.post_id == post_id
    )

    return db.scalar(stmt)


def count_likes(
    db: Session,
    post_id: int
):
    stmt = select(func.count()).where(
        Like.post_id == post_id
    )

    return db.scalar(stmt)


def get_post_likes(
    db: Session,
    post_id: int
):
    stmt = (
        select(User)
        .join(Like, Like.user_id == User.id)
        .where(Like.post_id == post_id)
    )

    return db.scalars(stmt).all()


def get_liked_posts_by_user(
    db: Session,
    user_id: int
):
    """Bir kullanıcının beğendiği tüm postları döner (sadece kendisi görebilir)."""
    stmt = (
        select(Post)
        .join(Like, Like.post_id == Post.id)
        .where(Like.user_id == user_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.topic),
        )
        .order_by(Like.created_at.desc())
    )

    return db.scalars(stmt).all()