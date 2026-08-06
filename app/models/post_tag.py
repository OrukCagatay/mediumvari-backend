from sqlalchemy.orm import Mapped,relationship
from sqlalchemy.orm import mapped_column
from datetime import datetime,timezone
from sqlalchemy import ForeignKey
from app.db.database import Base 



class PostTag(Base):

    __tablename__= "post_tags"

    
    post_id: Mapped[int]= mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int]= mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)