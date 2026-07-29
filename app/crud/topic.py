from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate


def get_topics(
    db: Session,
):
    stmt = (
        select(Topic)
        .order_by(Topic.name.asc())
    )

    return db.scalars(stmt).all()


def get_topic(
    db: Session,
    topic_id: int,
):
    stmt = (
        select(Topic)
        .where(Topic.id == topic_id)
    )

    return db.scalar(stmt)


def get_topic_by_name(
    db: Session,
    name: str,
):
    stmt = (
        select(Topic)
        .where(Topic.name == name)
    )

    return db.scalar(stmt)


def create_topic(
    db: Session,
    topic_data: TopicCreate,
):
    db_topic = Topic(name=topic_data.name)

    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)

    return db_topic


def update_topic(
    db: Session,
    topic: Topic,
    topic_data: TopicUpdate,
):
    topic.name = topic_data.name

    db.commit()
    db.refresh(topic)

    return topic


def delete_topic(
    db: Session,
    topic: Topic,
):
    db.delete(topic)
    db.commit()