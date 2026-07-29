from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from datetime import datetime,timezone
from sqlalchemy import ForeignKey

from app.db.database import Base 


class Like(Base):

    __tablename__ ="likes"

    user_id:Mapped[int]= mapped_column(ForeignKey("users.id"),primary_key=True)

    post_id: Mapped[int]= mapped_column(ForeignKey("posts.id"),primary_key=True)

    created_at: Mapped[datetime]= mapped_column(default=lambda:datetime.now(timezone.utc)) 