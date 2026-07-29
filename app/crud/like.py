from sqlalchemy.orm import Session
from sqlalchemy import select,func

from app.models.like import Like
from app.models.user import User

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
    user_id:int,
    post_id:int
):
    stmt = select(Like).where(
    Like.user_id == user_id,
    Like.post_id == post_id
)
    like = db.scalar(stmt)
    
    db.delete(like)
    db.commit()



def get_like(           # kullanıcı bu postu beğenmiş mi ??
    db: Session,
    user_id: int,
    post_id: int
):
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.post_id == post_id
    )

    return db.scalar(stmt)



def count_likes(        # like sayısı döner 
    db: Session,
    post_id: int
):
    stmt = select(func.count()).where(
        Like.post_id == post_id
    )

    return db.scalar(stmt)


def get_post_likes(
    db: Session,
    post_id: int        # kimlerin beğendiğini döner postu
):
    stmt = (
        select(User)
        .join(Like, Like.user_id == User.id)
        .where(Like.post_id == post_id)
    )

    return db.scalars(stmt).all()