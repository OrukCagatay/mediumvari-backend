from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import current_user
from app.models.user import User

from app.schemas.ai import (
    GenerateArticleRequest,
    GenerateArticleResponse
)

from app.services.ai import generate_article_service

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post(
    "/generate-article",
    response_model=GenerateArticleResponse,
    summary="Generate an AI article",
    description="""
Generate a complete Medium-style article using Google Gemini.

- Authentication required
- Daily AI usage limits apply
- Returns the generated article title and content
""",
    responses={
        429: {
            "description": "Daily AI request limit exceeded"
        },
        503: {
            "description": "AI service is unavailable"
        },
        504: {
            "description": "AI service timeout"
        }
    }
)
def generate_article(
    request: GenerateArticleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_user)
):
    return generate_article_service(
        db,
        request,
        current_user
    )