from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.follow import Follow



def get_following_feed(
    db: Session,
    current_user_id: int
):
    following_subquery = (
        select(Follow.following_id)
        .where(Follow.follower_id == current_user_id)
    )

    stmt = (
        select(Post)
        .where(Post.author_id.in_(following_subquery))
        .order_by(Post.created_at.desc())
    )

    return db.scalars(stmt).all()



def get_explore_feed(
    db: Session
):
    stmt = (
        select(Post)
        .order_by(Post.created_at.desc())
    )

    return db.scalars(stmt).all()