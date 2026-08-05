from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.user import User, UserRole
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like

from sqlalchemy.orm import Session

from app.crud.post import get_post
from app.crud.comment import get_comment


def get_all_users(
    db: Session,
):
    stmt = (
        select(User)
        .order_by(User.created_at.desc())
    )

    return db.scalars(stmt).all()


def get_user_by_id(
    db: Session,
    user_id: int,
):
    stmt = (
        select(User)
        .where(User.id == user_id)
    )

    return db.scalar(stmt)


def update_user_role(
    db: Session,
    user: User,
    role: UserRole,
):
    user.role = role

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
):
    db.delete(user)
    db.commit()



def admin_delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()



def admin_delete_comment(db: Session, comment: Comment):
    db.delete(comment)
    db.commit()



def get_dashboard_stats(
    db: Session,
):
    total_users = db.scalar(
        select(func.count(User.id))
    )

    total_posts = db.scalar(
        select(func.count(Post.id))
    )

    total_comments = db.scalar(
        select(func.count(Comment.id))
    )

    total_likes = db.scalar(
        select(func.count())
        .select_from(Like)
    )

    return {
        "total_users": total_users,
        "total_posts": total_posts,
        "total_comments": total_comments,
        "total_likes": total_likes,
    }