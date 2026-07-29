from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from datetime import datetime,timezone
from sqlalchemy import ForeignKey

from app.db.database import Base 



class Follow(Base):

    __tablename__ ="follows"

    follower_id:Mapped[int]= mapped_column(ForeignKey("users.id"),primary_key=True)
    following_id:Mapped[int]= mapped_column(ForeignKey("users.id"),primary_key=True)

    created_at: Mapped[datetime]= mapped_column(default=lambda:datetime.now(timezone.utc)) 