import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.topic import Topic
from app.models.user import User
from app.models.post import Post
from app.models.like import Like
from app.models.comment import Comment

from app.seed.topics import TOPICS
from app.seed.users import FAKE_USERS
from app.seed.posts import FAKE_POSTS

from app.core.security import password_hash

import random
from datetime import datetime, timedelta, timezone

from app.models.post import Post
from app.seed.language_test_posts import LANGUAGE_TEST_POSTS
from app.services.language_detection import detect_language


def seed_topics(db):
    for topic_name in TOPICS:
        exists = db.scalar(select(Topic).where(Topic.name == topic_name))
        if exists:
            continue
        db.add(Topic(name=topic_name))
    db.commit()


def seed_users(db):
    created_users = []
    for user_data in FAKE_USERS:
        exists = db.scalar(select(User).where(User.username == user_data["username"]))
        if exists:
            created_users.append(exists)
            continue

        user = User(
            username=user_data["username"],
            email=user_data["email"],
            bio=user_data["bio"],
            hashed_password=password_hash.hash("password123"),
        )
        db.add(user)
        db.flush()
        created_users.append(user)

    db.commit()
    return created_users


def seed_posts(db, users):
    topics = db.scalars(select(Topic)).all()
    topic_by_name = {t.name: t for t in topics}

    created_posts = []

    for i, post_data in enumerate(FAKE_POSTS):
        exists = db.scalar(select(Post).where(Post.title == post_data["title"]))
        if exists:
            created_posts.append(exists)
            continue

        author = users[i % len(users)]
        topic = topic_by_name.get(post_data["topic"])

        days_ago = random.randint(0, 60)
        created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)

        post = Post(
            title=post_data["title"],
            content=post_data["content"],
            author_id=author.id,
            topic_id=topic.id if topic else None,
            created_at=created_at,
        )
        db.add(post)
        db.flush()
        created_posts.append(post)

    db.commit()
    return created_posts


def seed_likes_and_comments(db, users, posts):
    comment_texts = [
        "Really well written, thanks for sharing.",
        "I disagree with part of this, but great points overall.",
        "This is exactly what I needed to read today.",
        "Do you have any sources for this?",
        "Saved this for later, great post.",
        "Interesting take, hadn't thought about it that way.",
        "This resonates with my own experience.",
        "Solid advice, going to try this.",
    ]

    for post in posts:
        likers = random.sample(users, k=random.randint(0, min(6, len(users))))
        for user in likers:
            exists = db.scalar(
                select(Like).where(Like.post_id == post.id, Like.user_id == user.id)
            )
            if exists:
                continue
            db.add(Like(post_id=post.id, user_id=user.id))

        commenters = random.sample(users, k=random.randint(0, 3))
        for user in commenters:
            db.add(
                Comment(
                    post_id=post.id,
                    user_id=user.id,
                    content=random.choice(comment_texts),
                )
            )

    db.commit()




def seed_language_test_posts(db, author_id: int, topic_id: int | None = None):
    created = []

    for i, post_data in enumerate(LANGUAGE_TEST_POSTS):
        exists = db.query(Post).filter(Post.title == post_data["title"]).first()
        if exists:
            created.append(exists)
            continue

        detected_language = detect_language(post_data["content"])

        # En yeniden en eskiye doğru, birbirinden farklı zaman damgaları
        created_at = datetime.now(timezone.utc) - timedelta(minutes=i * 5)

        post = Post(
            title=post_data["title"],
            content=post_data["content"],
            author_id=author_id,
            topic_id=topic_id,
            language=detected_language,
            created_at=created_at,
        )
        db.add(post)
        db.flush()
        created.append(post)

    db.commit()
    return created


def run_seed():
    db = SessionLocal()
    try:
        seed_topics(db)
        users = seed_users(db)
        posts = seed_posts(db, users)
        seed_likes_and_comments(db, users, posts)
        print(f"Seeded {len(users)} users, {len(posts)} posts, with likes and comments.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()