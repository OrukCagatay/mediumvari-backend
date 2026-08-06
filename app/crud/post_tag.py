from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.post_tag import PostTag


def create_post_tag(
    db: Session,
    post_id: int,
    tag_id: int
):
    existing = db.execute(
        select(PostTag).where(
            PostTag.post_id == post_id,
            PostTag.tag_id == tag_id,
        )
    ).scalar_one_or_none()

    if existing is not None:
        return existing

    db_post_tag = PostTag(
        post_id=post_id,
        tag_id=tag_id
    )

    db.add(db_post_tag)
    try:
        db.commit()
    except IntegrityError:
        # Paralel bir istek araya girip aynı satırı eklemiş olabilir — sorun değil, geri al ve devam et
        db.rollback()
        existing = db.execute(
            select(PostTag).where(
                PostTag.post_id == post_id,
                PostTag.tag_id == tag_id,
            )
        ).scalar_one_or_none()
        return existing

    db.refresh(db_post_tag)
    return db_post_tag