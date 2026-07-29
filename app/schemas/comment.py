from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

    user_id: int
    post_id: int

    model_config = {
        "from_attributes": True
    }


"""
Neden sadece content var?

Çünkü:

POST /posts/{post_id}/comments

isteğinde frontend sadece yorumu gönderir.

{
    "content": "Harika bir yazı olmuş."
}

user_id JWT'den gelir.

post_id URL'den gelir.

created_at database oluşturur.

id database oluşturur.

Dolayısıyla kullanıcı bunları göndermemelidir.

"""