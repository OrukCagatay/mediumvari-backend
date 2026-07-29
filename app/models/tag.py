from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.db.database import Base 



class Tag(Base):

    __tablename__="tags"

    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(unique=True,index=True)