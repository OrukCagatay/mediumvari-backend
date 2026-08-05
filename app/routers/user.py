from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status,Query

from app.db.database import get_db
from app.schemas.user import UserResponse,UserUpdate,PublicUserProfile
from app.models.user import User

from app.schemas.post import PostResponse
from app.schemas.comment import CommentResponse
from app.services.user import get_my_liked_posts_service, get_my_comments_service

from app.services.user import get_users_service,delete_user_service
from app.services.user import update_user_service

from app.services.user import get_user_service

from app.dependencies.auth import current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



"""Swagger │ ▼ JSON geliyor │ router ▼ pydantic/schema user: UserCreate (JSON doğrulanıyor) 
│ ▼ database db = Depends(get_db) (Session açılıyor) │ ▼ crud/create_user(db, user) (CRUD çalışıyor) │
 ▼ User objesi dönüyor │schema ▼ UserResponse'a çevriliyor │router/ ▼ JSON olarak kullanıcıya gönderiliyor"""

"""Swagger / Frontend----JSON isteği gelir---Router (POST /users)---Pydantic Schema (UserCreate)
→ Gelen JSON doğrulanır.
→ Geçersizse 422 hatası döner--  --Database (Depends(get_db)) → Yeni Session oluşturulur.
        │
CRUD (create_user(db, user))→ User nesnesi oluşturulur.→ db.add()→ db.commit()→ db.refresh() 
SQLAlchemy User objesi döner--Pydantic Schema (UserResponse)-Hassas alanlar (hashed_password vb.) çıkarılır.
Sadece döndürülmesi gereken alanlar bırakılır.
Router--JSON Response kullanıcıya gönderilir."""


@router.get("/", response_model=list[UserResponse])
def read_users(
    search: str | None = Query(None, description="Search users by username"),
    db: Session = Depends(get_db)
):
    return get_users_service(db, search)    # userları dönüyo liste liste crudddaki get user fonksiyonundan


@router.get("/me",response_model=UserResponse)
def get_me(
    current_user = Depends(current_user)      #kendi id sini döner
):
    return current_user     



@router.get("/{user_id}", response_model=PublicUserProfile)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_service(db, user_id)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_me_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)     # burada    endpoint çalışmadan önce jwt doğrulanır ve
):                                                      # current user nesnesi oluşur ,gerekirse service ordan da cruda iletir    
    delete_user_service(
        db,
        current_user
    )
                # buralarda hiç işlem yapmıyorum endpointi alıp service iletiyorum bak returne  


@router.put(
    "/me",
    response_model=UserResponse
)
def update_me_endpoint(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return update_user_service(
        db,
        current_user,
        user_data
    )



@router.get("/me/likes", response_model=list[PostResponse])
def get_my_likes(
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    
    return get_my_liked_posts_service(db, current_user)




@router.get("/me/comments", response_model=list[CommentResponse])
def get_my_comments(
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    
    return get_my_comments_service(db, current_user)




# user update delete de authorization işini hallet 


## update ederken sadece adını veya email  olmalı o kısmı tekrar ele al saçma çünkü