from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict,Field


class UserCreate(BaseModel):        #pydantic userdan gelen jsonı python objecte çevirir
    username: str =Field(
        min_length=3,
        max_length=30
    )
    email: EmailStr                 
    password: str  = Field(
        min_length=8,
        max_length=128
    )


class UserResponse(BaseModel):   #usera dönüt için lazım 
    id: int
    username: str
    email: EmailStr
    created_at: datetime
                                                        #sqlalchemy v2 ile gelen bişey
    model_config = ConfigDict(from_attributes=True) #burası sqlalchemy objesinin otomatik olarak api cevabına çevirebiliyor




class UserUpdate(BaseModel):    #update putla herşey update edilir ,patch yama istenilen gerisi opsiyonel
    username: str
    email: EmailStr



class UserLogin(BaseModel): #user login işi safe almak için
    email: EmailStr
    password: str



class Token(BaseModel):   #usera tokenli dönecek log inden sonra 
    access_token: str
    refresh_token: str
    token_type: str




class UserPreview(BaseModel):       # like atan userları gösttermek için var
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)



class RefreshTokenRequest(BaseModel):
    refresh_token: str