from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.topic import Topic

from app.seed.topics import TOPICS


def seed_topics():

    db = SessionLocal()

    try:

        for topic_name in TOPICS:

            exists = db.scalar(
                select(Topic).where(
                    Topic.name == topic_name
                )
            )

            if exists:
                continue

            db.add(
                Topic(
                    name=topic_name
                )
            )

        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed_topics()
    print("Topics seeded successfully.")