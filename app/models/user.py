from sqlalchemy.orm import Mapped,relationship
from sqlalchemy.orm import mapped_column
from datetime import datetime,timezone
from app.db.database import Base 
import sqlalchemy as sa
from enum import Enum


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import Post

    

class UserRole(str, Enum):
    user = "user"
    admin = "admin"



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )

    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole),
        default=UserRole.user,
        nullable=False
    )

    hashed_password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


