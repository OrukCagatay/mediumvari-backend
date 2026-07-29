from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.topic import (
    get_topics,
    get_topic,
    get_topic_by_name,
    create_topic,
    update_topic,
    delete_topic,
)

from app.schemas.topic import TopicCreate, TopicUpdate


def get_topics_service(
    db: Session,
):
    return get_topics(db)


def get_topic_service(
    db: Session,
    topic_id: int,
):
    topic = get_topic(
        db,
        topic_id
    )

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    return topic


def create_topic_service(
    db: Session,
    topic_data: TopicCreate,
):
    existing = get_topic_by_name(db, topic_data.name)

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A topic with this name already exists"
        )

    return create_topic(db, topic_data)


def update_topic_service(
    db: Session,
    topic_id: int,
    topic_data: TopicUpdate,
):
    topic = get_topic(db, topic_id)

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    existing = get_topic_by_name(db, topic_data.name)

    if existing is not None and existing.id != topic_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A topic with this name already exists"
        )

    return update_topic(db, topic, topic_data)


def delete_topic_service(
    db: Session,
    topic_id: int,
):
    topic = get_topic(db, topic_id)

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    delete_topic(db, topic)

    return {
        "message": "Topic deleted successfully"
    }