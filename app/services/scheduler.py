from apscheduler.schedulers.background import BackgroundScheduler

from app.db.database import SessionLocal
from app.services.trending import refresh_trending_cache


def _scheduled_trending_refresh():
    db = SessionLocal()
    try:
        refresh_trending_cache(db)
        print("[SCHEDULER] Trending cache refreshed")
    except Exception as e:
        print(f"[SCHEDULER] Failed to refresh trending cache: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(_scheduled_trending_refresh, 'interval', hours=1, id='trending_refresh')
    scheduler.start()
    return scheduler