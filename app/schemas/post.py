from pydantic import BaseModel,Field
from datetime import datetime
from enum import Enum

from app.schemas.topic import TopicResponse

class PostCreate(BaseModel):
    title: str
    content: str
    topic_id: int
    tags: list[str]



class PostResponse(BaseModel):
    id: int
    title: str                  # comment ekledikten sonra feedi yaparken post response advenced edilecek halledilecek 
    content: str
    created_at: datetime
    author_id: int              #author id postCreate de var ama response modelinde yok çünkü jwtden alacağız.
    topic: TopicResponse | None

    model_config = {
        "from_attributes": True
    }   
                                 


class PostUpdate(BaseModel):
    title: str =Field(
        min_length=3,
        max_length=200
    )
    content: str =Field(
        min_length=10,
        max_length=5000
    )
    topic_id: int


class PostSortBy(str, Enum):
    newest = "newest"
    oldest = "oldest"
    most_liked = "most_liked"