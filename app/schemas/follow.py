
from pydantic import BaseModel


class FollowResponse(BaseModel):

    message:str



class FollowCountResponse(BaseModel):
    
    count: int