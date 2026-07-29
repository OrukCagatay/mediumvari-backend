from sqlalchemy.orm import Mapped,relationship
from sqlalchemy.orm import mapped_column
from datetime import datetime,timezone
from sqlalchemy import ForeignKey
from app.db.database import Base 


class Comment(Base):

    __tablename__="comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    content: Mapped[str]
    created_at: Mapped[datetime]= mapped_column(default=lambda:datetime.now(timezone.utc)) 

    user_id :Mapped[int]= mapped_column(ForeignKey("users.id"))
    post_id :Mapped[int]= mapped_column(ForeignKey("posts.id"))

    

# neden like gibi composite key değil user_id ile post_id çünkü bir kullanıcı bir
#   postu en çok bir kez beğenebilir  ama bir user bir posta istediği kadar yorum atabilir 
# o yüzden user ve post id foreign key olur 
    

# Like modelindeki gibi composite primary key kullanmıyoruz.
#
# Çünkü bir kullanıcı bir postu yalnızca bir kez beğenebilir.
# Bu yüzden (user_id, post_id) çifti benzersizdir ve composite
# primary key olarak kullanılabilir.
#
# Ancak bir kullanıcı aynı posta birden fazla yorum yapabilir.
# Bu nedenle (user_id, post_id) benzersiz değildir.
#
# Bu yüzden her Comment'ın kendine ait bir id'si bulunur,
# user_id ve post_id ise sadece Foreign Key olarak tutulur.