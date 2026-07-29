from enum import Enum

from pydantic import BaseModel, Field


class ArticleTone(str, Enum):
    professional = "professional"
    friendly = "friendly"
    casual = "casual"
    technical = "technical"
    educational = "educational"
    storytelling = "storytelling"


class TargetAudience(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class ArticleType(str, Enum):
    tutorial = "tutorial"
    guide = "guide"
    opinion = "opinion"
    comparison = "comparison"
    deep_dive = "deep_dive"
    listicle = "listicle"


class ReadingTime(str, Enum):
    min3 = "3 min"
    min5 = "5 min"
    min8 = "8 min"
    min15 = "15 min"


READING_TIME_WORD_COUNTS = {
    ReadingTime.min3: 600,
    ReadingTime.min5: 1000,
    ReadingTime.min8: 1600,
    ReadingTime.min15: 2800,
}


class GenerateArticleRequest(BaseModel):

    article_topic: str = Field(min_length=5, max_length=300,description="Main subject of the article")

    tone: ArticleTone = ArticleTone.professional
    custom_tone: str | None = Field(default=None, max_length=300)

    audience: TargetAudience = TargetAudience.intermediate
    custom_audience: str | None = Field(default=None, max_length=300)

    article_type: ArticleType = ArticleType.guide
    custom_article_type: str | None = Field(default=None, max_length=300)

    reading_time: ReadingTime = ReadingTime.min5

    language: str = "English"
    custom_language: str | None = Field(default=None, max_length=100)

    keywords: list[str] = Field(default_factory=list, max_length=10)

    include_code: bool = True
    include_examples: bool = True
    include_seo: bool = False

    additional_instructions: str | None = Field(default=None, max_length=500)


    model_config = {
    "json_schema_extra": {
        "example": {
            "article_topic": "Oppenheimer: Historical Accuracy vs Christopher Nolan's Vision",
            "tone": "professional",
            "audience": "intermediate",
            "article_type": "comparison",
            "reading_time": "5 min",
            "language": "Turkish",
            "keywords": [
                "Oppenheimer",
                "Christopher Nolan",
                "History"
            ],
            "include_code": False,
            "include_examples": True,
            "include_seo": True,
            "additional_instructions": "Compare historical facts with the movie adaptation."
        }
    }
}


class SEOMeta(BaseModel):
    title: str
    meta_description: str
    tags: list[str] = Field(default_factory=list)


class GenerateArticleResponse(BaseModel):
    title: str
    excerpt: str
    content: str
    seo: SEOMeta | None = None
    is_uncertain: bool = False