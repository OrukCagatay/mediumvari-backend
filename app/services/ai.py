import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.ai import GenerateArticleRequest, GenerateArticleResponse, SEOMeta

from app.ai.prompt_builder import build_article_prompt
from app.ai.gemini import generate_text
from app.ai.exceptions import (
    GeminiAPIError,
    GeminiTimeoutError,
    GeminiEmptyResponseError,
)

from app.crud.ai_usage import count_requests_today, log_usage
from app.core.config import AI_DAILY_REQUEST_LIMIT


def _parse_article(raw_text: str) -> GenerateArticleResponse:
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI servisi geçersiz bir format döndürdü, lütfen tekrar deneyin."
        )

    seo_data = data.get("seo")
    seo = SEOMeta(**seo_data) if seo_data else None

    return GenerateArticleResponse(
        title=data.get("title", "Untitled"),
        excerpt=data.get("excerpt", ""),
        content=data.get("content", ""),
        is_uncertain=data.get("is_uncertain", False),
        seo=seo,
    )

def generate_article_service(
    db: Session,
    request: GenerateArticleRequest,
    current_user: User
) -> GenerateArticleResponse:

    used_today = count_requests_today(db, current_user.id)

    if used_today >= AI_DAILY_REQUEST_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Günlük AI kullanım limitiniz doldu ({AI_DAILY_REQUEST_LIMIT} istek)."
        )

    prompt = build_article_prompt(request)

    try:
        raw_text = generate_text(prompt)

    except GeminiTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="AI servisi zamanında yanıt vermedi, lütfen tekrar deneyin."
        )

    except GeminiEmptyResponseError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI servisi geçerli bir içerik üretemedi."
        )

    except GeminiAPIError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI servisi şu anda kullanılamıyor, lütfen daha sonra tekrar deneyin."
        )

    log_usage(db, current_user.id)

    return _parse_article(raw_text)