from sqlalchemy.orm import Session

from app.models.post_tag import PostTag



def create_post_tag(
    db: Session,
    post_id: int,
    tag_id: int
):
    db_post_tag = PostTag(
        post_id=post_id,
        tag_id=tag_id
    )

    db.add(db_post_tag)
    db.commit()
    db.refresh(db_post_tag)

    return db_post_tag