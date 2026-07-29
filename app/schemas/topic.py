from pydantic import BaseModel, Field


class TopicResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class TopicCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class TopicUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50)