from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import UserPreview


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

    author: UserPreview
    post_id: int

    model_config = {
        "from_attributes": True
    }