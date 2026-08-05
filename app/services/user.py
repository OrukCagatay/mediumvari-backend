from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.like import get_liked_posts_by_user
from app.crud.comment import get_comments_by_user

from app.schemas.user import UserCreate
from app.crud.user import get_users,get_user
from app.crud.user import delete_user,update_user,UserUpdate

from app.models.user import User



"""Router → create_user_service() → try → create_user() → db.commit() →
 Başarılı: User döner | Hata: IntegrityError →
 Service yakalar → rollback() → HTTPException(409) → Router → Client"""

#cruddaki her şeyi service getiriyorum ister http eskiden olsun ya da olmasın

def get_users_service(db: Session, search: str | None = None):
    return get_users(db, search)


def get_user_service(
    db: Session,
    user_id: int
):

    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def update_user_service(
    db: Session,
    current_user: User,
    user_data: UserUpdate
):
    try:
        return update_user(
            db,
            current_user,
            user_data
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )


def delete_user_service(
    db: Session,
    current_user: User
):
    delete_user(
        db,
        current_user
    )



def get_my_liked_posts_service(db: Session, current_user: User):

    return get_liked_posts_by_user(db, current_user.id)



def get_my_comments_service(db: Session, current_user: User):

    return get_comments_by_user(db, current_user.id)