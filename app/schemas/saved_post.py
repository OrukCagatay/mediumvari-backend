from pydantic import BaseModel


class SavedPostResponse(BaseModel):
    message: str