from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy.orm import Mapped

from app.db.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import Post

class Topic(Base):


    __tablename__="topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(unique=True,index=True)


    posts: Mapped[list["Post"]] = relationship(
    back_populates="topic"
)