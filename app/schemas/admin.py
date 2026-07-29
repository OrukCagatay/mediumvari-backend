from pydantic import BaseModel


from app.models.user import UserRole



class DashboardResponse(BaseModel):
    total_users: int
    total_posts: int
    total_comments: int
    total_likes: int



class UserRoleUpdate(BaseModel):
    role: UserRole