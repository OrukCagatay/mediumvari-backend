# Mediumvari — Backend

A full-featured **Medium-inspired publishing platform backend** built with **FastAPI**. Mediumvari goes beyond a traditional blogging API by integrating **AI-assisted content generation**, **multilingual translation**, **text-to-speech podcast generation**, **Redis-powered trending posts**, and a **fully containerized deployment**.

---

# Features

## Core Platform

- JWT authentication (Access & Refresh Tokens)
- Refresh token blacklisting on logout
- Role-based authorization (User / Admin)
- Post CRUD with Draft & Published states
- Comments, Likes and Follow system
- Saved Posts
- Search, sorting and pagination
- Personalized Feed & Explore pages
- Admin dashboard
  - User management
  - Content moderation
  - Platform statistics

---

## AI Features

### AI Article Generation

Generate complete Medium-style articles using **Google Gemini**. Supports:

- Topic-based generation
- Writing tone
- Target audience
- Article length
- SEO keywords
- SEO metadata

---

### AI Translation

Automatic language detection using **langdetect**. Posts can be translated into:

- English
- Turkish
- French
- German

using **deep-translator**. Translations are generated asynchronously and stored independently.

---

### AI Podcast Generation

Generate natural-sounding podcasts from articles using **Edge TTS**. Features:

- Multiple languages
- Background generation using FastAPI BackgroundTasks
- Minimum word count validation
- On-demand regeneration

---

## Content Versioning

Mediumvari prevents stale AI-generated content. Whenever a post is edited:

- Existing translations are marked as **Outdated**
- Existing podcasts are marked as **Outdated**
- Old generated content is never served to readers
- Authors can regenerate translations or podcasts whenever they want

This keeps generated AI content synchronized with the latest version of the article while avoiding unnecessary API costs.

---

## Media

Images are stored on **Cloudinary**. Supports:

- Automatic optimization
- Dynamic resizing
- Format conversion
- Quality transformations

---

## Performance

Trending posts are powered by **Redis**. Every hour:

- APScheduler calculates the **Top 10 most-liked posts in the last 24 hours**
- Results are cached in Redis
- Cache TTL: **15 minutes**

This avoids expensive database queries on every request while keeping trending posts nearly real-time.

---

## Infrastructure

- Docker
- Docker Compose
- Alembic database migrations
- SQLite (development)
- Foreign key integrity enabled (`PRAGMA foreign_keys=ON`)

---

# Tech Stack

| Layer | Technology |
|--------|------------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Database | SQLite |
| Authentication | JWT (PyJWT) |
| Password Hashing | Argon2id |
| AI | Google Gemini |
| Translation | deep-translator |
| Text-to-Speech | edge-tts |
| Cache | Redis |
| Scheduler | APScheduler |
| Media Storage | Cloudinary |
| Containerization | Docker & Docker Compose |

---

# Project Structure

```
app/
│
├── ai/              # AI generation logic (Gemini prompt building, response parsing)
├── core/            # Configuration, security, Redis client, Cloudinary config
├── crud/            # Database access layer (one file per resource)
├── db/              # Engine, Session, Base model
├── dependencies/    # Authentication dependencies (CurrentUser, OptionalCurrentUser)
├── models/          # SQLAlchemy ORM models
├── routers/         # API endpoint definitions
├── schemas/         # Pydantic request/response schemas
├── services/        # Business logic layer
├── seed/            # Seed data utilities
├── utils/           # Shared helper functions
└── main.py          # App entrypoint, middleware, router registration

alembic/
└── versions/        # Database migration history

seed_bot.py           # Load-testing / demo data generator
test_ai.py             # AI generation testing script
Dockerfile
docker-compose.yml
```

---

# Architecture

Mediumvari follows a layered architecture:

```
Client
  │
  ▼
Router
  │
  ▼
Service
  │
  ▼
CRUD
  │
  ▼
Database
```

### Responsibilities

**Router**
- HTTP endpoints
- Request validation
- Response serialization

**Service**
- Business logic
- Authorization
- AI orchestration
- External service integrations

**CRUD**
- Thin reusable database queries
- No business logic

---

# Getting Started

## Prerequisites

- Python 3.13+
- Docker & Docker Compose (recommended)

---

# Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
SECRET_KEY=your_jwt_secret
```

---

# Run with Docker

```bash
docker-compose up --build
```

Services:

- Backend → http://localhost:8000
- Swagger Docs → http://localhost:8000/docs
- Frontend → http://localhost:3000

---

# Run Locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate (Windows):

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Run Redis separately if Docker is not being used:

```bash
docker run -d --name mediumvari-redis -p 6379:6379 redis:alpine
```

---

# Seed Demo Data

Populate the database with realistic test data. The seed bot creates:

- 100 users
- 200 posts
- Random likes
- Random comments
- Random follows

Run:

```bash
uvicorn app.main:app
```

then

```bash
python seed_bot.py
```

---

# API Documentation

Interactive Swagger documentation is available at:

```
http://localhost:8000/docs
```

It includes all endpoints for:

- Authentication
- Users
- Posts
- Comments
- Likes
- Follows
- Topics
- Saved Posts
- Feed
- Explore
- Admin
- AI Generation
- Translation
- Podcast
- Image Upload
- Trending Posts

---

# Related Projects

**Frontend** — https://github.com/OrukCagatay/mediumvari-frontend