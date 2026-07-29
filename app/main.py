from fastapi import FastAPI
from app import models
from app.routers.user import router as user_router
from app.routers.post import router as post_router 
from app.routers.like import router as like_router
from app.routers.comment import router as comment_router
from app.routers.follow import router as follow_router
from app.routers.feed import router as feed_router
from app.routers.saved_post import router as saved_post_router
from app.routers.auth import router as auth_router
from app.routers.topic import router as topic_router
from app.routers.ai import router as ai_router
from app.routers.admin import router as admin_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(follow_router)
app.include_router(feed_router)
app.include_router(saved_post_router)
app.include_router(topic_router)
app.include_router(ai_router)