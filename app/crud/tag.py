from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag


def get_tag_by_name(
    db: Session,
    name: str
):
    stmt = select(Tag).where(Tag.name == name)

    return db.scalar(stmt)


def create_tag(
    db: Session,
    name: str
):
    db_tag = Tag(
        name=name
    )

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag