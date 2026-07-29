from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped,relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime,timezone


from app.db.database import Base 

if TYPE_CHECKING:
    from app.models.user import User


if TYPE_CHECKING:
    from app.models.topic import Topic


class Post(Base):
    
    __tablename__ ="posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime]= mapped_column(default=lambda:datetime.now(timezone.utc)) #zamanı otomatik atasın diye 
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True) # bu da db ye der sil diye 
    topic_id :Mapped[int] = mapped_column(ForeignKey("topics.id"),nullable=True,index=True)

    author: Mapped["User"] = relationship(
    back_populates="posts")


    topic: Mapped["Topic"] = relationship(
    back_populates="posts")