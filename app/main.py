from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

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
from app.routers.health import router as health_router
from app.routers.image import router as image_router
from app.routers.post_translation import router as post_translation_router
from app.routers.trending import router as trending_router

from app.services.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],   
)


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(trending_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(follow_router)
app.include_router(feed_router)
app.include_router(saved_post_router)
app.include_router(topic_router)
app.include_router(ai_router)
app.include_router(health_router)
app.include_router(image_router)
app.include_router(post_translation_router)
