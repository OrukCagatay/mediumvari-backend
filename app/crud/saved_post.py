from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.saved_post import SavedPost
from app.models.post import Post


def save_post(
    db: Session,
    user_id: int,
    post_id: int
):
    db_saved_post = SavedPost(
        user_id=user_id,
        post_id=post_id
    )

    db.add(db_saved_post)
    db.commit()
    db.refresh(db_saved_post)

    return db_saved_post


def unsave_post(
    db: Session,
    saved_post: SavedPost
):
    db.delete(saved_post)
    db.commit()




def get_saved_post(         #service buna bakarak daha önceden kaydedilmiş mi onu anlayacak 
    db: Session,
    user_id: int,
    post_id: int
):
    stmt = (
        select(SavedPost)
        .where(
            SavedPost.user_id == user_id,
            SavedPost.post_id == post_id
        )
    )

    return db.scalar(stmt)



def get_saved_posts(
    db: Session,
    user_id: int
):
    stmt = (
        select(Post)
        .join(
            SavedPost,
            Post.id == SavedPost.post_id
        )
        .where(
            SavedPost.user_id == user_id
        )
        .order_by(Post.created_at.desc())
    )

    return db.scalars(stmt).all()