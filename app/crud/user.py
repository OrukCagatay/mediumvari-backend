#crud verştabanı işlerini router ise http işlerini halleder

from sqlalchemy.orm import Session
from sqlalchemy import select


from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate


from app.core.security import password_hash



def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,

       
        hashed_password=password_hash.hash(user.password)
    )

    db.add(db_user)
    db.commit()
    
    db.refresh(db_user)

    return db_user


def get_users(db: Session, search: str | None = None):
    stmt = select(User)

    if search:
        stmt = stmt.where(User.username.ilike(f"%{search}%"))

    return db.scalars(stmt).all()


def get_user(db: Session, user_id: int):

    stmt = select(User).where(User.id == user_id)

    user = db.scalar(stmt)

    return user


def delete_user(
    db: Session,
    user: User
):
    db.delete(user)
    db.commit()


    
def update_user(
    db: Session,
    user: User,
    user_data: UserUpdate
):
    user.username = user_data.username
    user.email = user_data.email
    user.bio = user_data.bio

    db.commit()
    db.refresh(user)

    return user



def get_user_by_email(
    db: Session,
    email: str
):
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)



    """jwt nin olayı sen login yapınca sana bi identifier verir token her işleminde isteğinde senin kim olduğunu bunun ile bilir 
    normalde http stateless yani her istek bağımsız seni takığ edemez ama jtw ile takip eder ,
    
    JWT, kullanıcının sisteme giriş yaptıktan sonra kimliğini kanıtlamasını sağlar. Böylece server, 
    her istekte kullanıcının kim olduğunu bilir ve yetkilerine göre işlem yapar.
    
    Login → "Sen gerçekten Çağatay mısın?"
    JWT → "Tamam, sen Çağatay'sın."
    Authorization → "Çağatay olarak bu işlemi yapmaya yetkin var mı?"   """

# genel olarak router-- services---crud ---dbase