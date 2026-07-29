from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime,timezone
from app.db.database import Base 

class BlacklistedToken(Base):

    __tablename__="blacklisted_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    jti: Mapped[str] = mapped_column(unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    created_at: Mapped[datetime]= mapped_column(default=lambda:datetime.now(timezone.utc)) 