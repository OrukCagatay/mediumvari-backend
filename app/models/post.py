from typing import TYPE_CHECKING
from enum import Enum

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
import sqlalchemy as sa
from datetime import datetime, timezone


from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User


if TYPE_CHECKING:
    from app.models.topic import Topic


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


class Post(Base):

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=True, index=True)

    language: Mapped[str] = mapped_column(default="en", nullable=False)
    cover_image_url: Mapped[str | None] = mapped_column(nullable=True)
    version: Mapped[int] = mapped_column(default=1, nullable=False)

    status: Mapped[PostStatus] = mapped_column(
        sa.Enum(PostStatus),
        default=PostStatus.published,
        nullable=False,
        index=True,
    )

    author: Mapped["User"] = relationship(
        back_populates="posts")

    topic: Mapped["Topic"] = relationship(
        back_populates="posts")