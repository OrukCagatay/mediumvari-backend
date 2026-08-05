from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

from app.schemas.topic import TopicResponse
from app.schemas.user import UserPreview


class PostStatus(str, Enum):
    draft = "draft"
    published = "published"


class PodcastStatus(str, Enum):
    none = "none"
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    outdated = "outdated"


class PostCreate(BaseModel):
    title: str
    content: str
    topic_id: int
    tags: list[str]
    status: PostStatus = PostStatus.published
    cover_image_url: str | None = Field(default=None, max_length=2048)
    translation_languages: list[str] = Field(default_factory=list)
    podcast_languages: list[str] = Field(default_factory=list)


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: UserPreview
    topic: TopicResponse | None
    status: PostStatus
    cover_image_url: str | None
    language: str
    version: int

    model_config = {
        "from_attributes": True
    }


class PostUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10, max_length=5000)
    topic_id: int
    cover_image_url: str | None = Field(default=None, max_length=2048)


class PostSortBy(str, Enum):
    newest = "newest"
    oldest = "oldest"
    most_liked = "most_liked"