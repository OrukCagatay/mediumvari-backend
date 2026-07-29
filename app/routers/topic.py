from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.admin import admin_authenticator
from app.models.user import User

from app.schemas.topic import TopicResponse, TopicCreate, TopicUpdate

from app.services.topic import (
    get_topics_service,
    get_topic_service,
    create_topic_service,
    update_topic_service,
    delete_topic_service,
)

router = APIRouter(
    prefix="/topics",
    tags=["Topics"]
)


@router.get(
    "/",
    response_model=list[TopicResponse],
    summary="Get all topics"
)
def get_all_topics(
    db: Session = Depends(get_db)
):
    return get_topics_service(db)


@router.get(
    "/{topic_id}",
    response_model=TopicResponse,
    summary="Get topic by ID",
    responses={
        404: {"description": "Topic not found"}
    }
)
def get_single_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    return get_topic_service(db, topic_id)


@router.post(
    "/",
    response_model=TopicResponse,
    summary="Create a new topic",
    description="""
Creates a new topic.

Admin only.
""",
    responses={
        409: {"description": "A topic with this name already exists"}
    }
)
def create_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),
):
    return create_topic_service(db, topic_data)


@router.put(
    "/{topic_id}",
    response_model=TopicResponse,
    summary="Update a topic",
    description="""
Updates an existing topic.

Admin only.
""",
    responses={
        404: {"description": "Topic not found"},
        409: {"description": "A topic with this name already exists"},
    }
)
def update_topic(
    topic_id: int,
    topic_data: TopicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),
):
    return update_topic_service(db, topic_id, topic_data)


@router.delete(
    "/{topic_id}",
    summary="Delete a topic",
    description="""
Deletes a topic.

Admin only.
""",
    responses={
        404: {"description": "Topic not found"}
    }
)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_authenticator),
):
    return delete_topic_service(db, topic_id)