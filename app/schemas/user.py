from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    bio: str | None
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicUserProfile(BaseModel):
    """Başka bir kullanıcının profilini görüntülerken kullanılır (email gizli)."""
    id: int
    username: str
    bio: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    bio: str | None = Field(default=None, max_length=500)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserPreview(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    refresh_token: str