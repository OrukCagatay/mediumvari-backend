from typing import TYPE_CHECKING
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
import sqlalchemy as sa

from app.db.database import Base
from app.models.post import PodcastStatus

if TYPE_CHECKING:
    from app.models.post import Post


class TranslationStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    outdated = "outdated"


class PostTranslation(Base):

    __tablename__ = "post_translations"
    __table_args__ = (
        UniqueConstraint("post_id", "language", name="uq_post_translations_post_id_language"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    language: Mapped[str]

    translated_title: Mapped[str | None] = mapped_column(nullable=True)
    translated_content: Mapped[str | None] = mapped_column(nullable=True)
    translation_status: Mapped[TranslationStatus] = mapped_column(
        sa.Enum(TranslationStatus),
        default=TranslationStatus.pending,
        nullable=False,
    )

    audio_url: Mapped[str | None] = mapped_column(nullable=True)
    podcast_status: Mapped[PodcastStatus] = mapped_column(
        sa.Enum(PodcastStatus),
        default=PodcastStatus.none,
        nullable=False,
    )

    source_version: Mapped[int] = mapped_column(default=1, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    post: Mapped["Post"] = relationship()