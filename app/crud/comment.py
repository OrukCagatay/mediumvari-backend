from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.comment import Comment


def create_comment(
    db: Session,
    content: str,
    user_id: int,
    post_id: int
):
    db_comment = Comment(
        content=content,
        user_id=user_id,
        post_id=post_id
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def get_comment(
    db: Session,
    comment_id: int
):
    stmt = select(Comment).where(
        Comment.id == comment_id
    )

    return db.scalar(stmt)


def get_post_comments(
    db: Session,
    post_id: int
):
    stmt = (
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
    )

    return db.scalars(stmt).all()


def get_comments_by_user(
    db: Session,
    user_id: int
):
    """Bir kullanıcının tüm yorumlarını döner (sadece kendisi görebilir)."""
    stmt = (
        select(Comment)
        .where(Comment.user_id == user_id)
        .order_by(Comment.created_at.desc())
    )

    return db.scalars(stmt).all()


def update_comment(
    db: Session,
    comment: Comment,
    content: str
):
    comment.content = content

    db.commit()
    db.refresh(comment)

    return comment


def delete_comment(
    db: Session,
    comment: Comment
):
    db.delete(comment)
    db.commit()