"""
Test/Seed Bot (hardened) — 100 kullanıcı, 200 post, paralel like/comment/follow.
Bağlantı hatalarına ve backend hatalarına karşı dayanıklı — script asla çökmez,
sadece başarısız işlemleri sessizce sayar ve devam eder.

Çalıştırmadan önce backend'in --reload OLMADAN çalıştığından emin olun:
    uvicorn app.main:app

Kullanım:
    python seed_bot.py
"""

import random
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter

BASE_URL = "http://localhost:8000"
PASSWORD = "TestPass123!"
MAX_WORKERS = 10
TIMEOUT = 10

session = requests.Session()
adapter = HTTPAdapter(pool_connections=MAX_WORKERS, pool_maxsize=MAX_WORKERS * 2)
session.mount("http://", adapter)
session.mount("https://", adapter)

POST_TEMPLATES = [
    ("The Future of Remote Work", "Remote work has fundamentally changed how companies operate. Many organizations now offer hybrid models, balancing flexibility with in-person collaboration."),
    ("Five Books That Changed My Perspective", "Reading widely exposes you to ideas you would never encounter otherwise. These five books reshaped how I think about work and personal growth."),
    ("Why I Started Running Every Morning", "A year ago I could barely run a mile. Today, running is the first thing I do every day."),
    ("A Beginners Guide to Sourdough Bread", "Making sourdough seemed intimidating at first, but it's really about patience and consistency."),
    ("Exploring Southeast Asia on a Budget", "Traveling through Vietnam, Thailand, and Cambodia taught me that budget travel doesn't mean sacrificing experiences."),
    ("The Science of Good Sleep", "Sleep quality affects nearly every aspect of daily life, from mood to productivity."),
    ("Learning to Cook After Moving Out", "Nobody teaches you how to cook for one person. Here are the lessons I learned the hard way."),
    ("Why Minimalism Is Not About Owning Less", "Minimalism gets reduced to owning fewer things, but the real shift is about intention."),
    ("My First Year as a Freelancer", "Freelancing looked glamorous from the outside. The reality involved a lot of uncertainty."),
    ("The Case for Walking Meetings", "Some of my best ideas have come not at my desk but on a walk with no destination."),
    ("How I Finally Understood Investing", "Personal finance felt overwhelming until I broke it down into a few simple principles."),
    ("Raising a Toddler Taught Me Patience", "Before I had kids, I considered myself a fairly patient person. Then my daughter turned two."),
    ("A Skeptics Guide to Astrology", "I don't believe the stars determine anything, but I've come to appreciate astrology as a shared language."),
    ("The Hidden Cost of Multitasking", "Multitasking feels productive but the research says otherwise."),
    ("Why I Quit Social Media for a Month", "Deleting every app for thirty days revealed how much of my day had quietly been absorbed."),
    ("Building a Reading Habit That Sticks", "I used to buy books and never finish them. Changing a few small habits made reading a daily part of my life."),
    ("What Chess Taught Me About Decision Making", "Chess forces you to think several moves ahead, but also to accept some decisions are irreversible."),
    ("The Underrated Skill of Active Listening", "Most conversations are two people waiting for their turn to talk."),
    ("Why I Switched to a Standing Desk", "Six months in, here's an honest review of what changed and what didn't."),
    ("Notes on Learning a Language as an Adult", "Learning Spanish in my thirties is nothing like the language classes I took in school."),
]

COMMENT_TEMPLATES = [
    "Great read, thanks for sharing!",
    "This really resonated with me.",
    "Interesting perspective, though I see it differently.",
    "Well written, learned something new today.",
    "Exactly what I needed to read right now.",
    "Bookmarking this for later.",
    "Really well explained, thank you.",
    "This changed how I think about the topic.",
    "Solid points, especially the third one.",
    "Never thought about it this way before.",
]

TAG_POOL = ["life", "productivity", "personal", "learning", "reflection", "travel", "health", "growth"]


def register_and_login(index: int):
    username = f"testuser{index}"
    email = f"testuser{index}@example.com"

    try:
        reg_resp = session.post(f"{BASE_URL}/auth/register", json={
            "username": username, "email": email, "password": PASSWORD,
        }, timeout=TIMEOUT)
        if reg_resp.status_code not in (200, 201):
            return None

        login_resp = session.post(f"{BASE_URL}/auth/login", json={
            "email": email, "password": PASSWORD,
        }, timeout=TIMEOUT)
        if login_resp.status_code != 200:
            return None

        data = login_resp.json()
        return {
            "id": reg_resp.json().get("id"),
            "username": username,
            "token": data["access_token"],
        }
    except Exception:
        return None


def create_users_parallel(count: int):
    print(f"\n=== Creating {count} users (parallel) ===")
    users = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(register_and_login, i): i for i in range(1, count + 1)}
        done = 0
        for future in as_completed(futures):
            result = future.result()
            if result:
                users.append(result)
            done += 1
            if done % 20 == 0:
                print(f"  Processed {done}/{count}")
    print(f"  Done. {len(users)}/{count} users created.")
    return users


def get_topic_ids():
    try:
        resp = session.get(f"{BASE_URL}/topics/", timeout=TIMEOUT)
        if resp.status_code != 200:
            return [1]
        ids = [t["id"] for t in resp.json()]
        return ids if ids else [1]
    except Exception:
        return [1]


def create_one_post(user, topic_ids):
    try:
        headers = {"Authorization": f"Bearer {user['token']}"}
        title, content = random.choice(POST_TEMPLATES)
        resp = session.post(f"{BASE_URL}/posts/", headers=headers, json={
            "title": title,
            "content": content,
            "topic_id": random.choice(topic_ids),
            "tags": random.sample(TAG_POOL, k=2),
            "status": "published",
            "translation_languages": [],
            "podcast_languages": [],
        }, timeout=TIMEOUT)
        if resp.status_code in (200, 201):
            data = resp.json()
            return {"id": data["id"], "author_id": user["id"]}
        return None
    except Exception:
        return None


def create_posts_parallel(users: list, topic_ids: list, posts_per_user: int = 2):
    print(f"\n=== Creating {posts_per_user} posts per user (parallel) ===")
    tasks = [(user, topic_ids) for user in users for _ in range(posts_per_user)]
    posts = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(create_one_post, u, t) for u, t in tasks]
        done = 0
        for future in as_completed(futures):
            result = future.result()
            if result:
                posts.append(result)
            done += 1
            if done % 40 == 0:
                print(f"  Processed {done}/{len(tasks)}")
    print(f"  Done. {len(posts)} posts created.")
    return posts


def do_like(user, post):
    try:
        headers = {"Authorization": f"Bearer {user['token']}"}
        resp = session.post(f"{BASE_URL}/posts/{post['id']}/like", headers=headers, timeout=TIMEOUT)
        return resp.status_code in (200, 201, 204)
    except Exception:
        return False


def add_likes_parallel(users: list, posts: list, min_likes=5, max_likes=15):
    print("\n=== Adding likes (parallel) ===")
    tasks = []
    for user in users:
        others = [p for p in posts if p["author_id"] != user["id"]]
        if not others:
            continue
        n = min(random.randint(min_likes, max_likes), len(others))
        for post in random.sample(others, k=n):
            tasks.append((user, post))

    success, errors = 0, 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(do_like, u, p) for u, p in tasks]
        done = 0
        for future in as_completed(futures):
            if future.result():
                success += 1
            else:
                errors += 1
            done += 1
            if done % 100 == 0:
                print(f"  Processed {done}/{len(tasks)}")
    print(f"  Done. {success} likes added, {errors} errors.")
    return success, errors


def do_comment(user, post):
    try:
        headers = {"Authorization": f"Bearer {user['token']}"}
        resp = session.post(f"{BASE_URL}/comments/posts/{post['id']}", headers=headers,
                             json={"content": random.choice(COMMENT_TEMPLATES)}, timeout=TIMEOUT)
        return resp.status_code in (200, 201)
    except Exception:
        return False


def add_comments_parallel(users: list, posts: list, min_c=3, max_c=8):
    print("\n=== Adding comments (parallel) ===")
    tasks = []
    for user in users:
        others = [p for p in posts if p["author_id"] != user["id"]]
        if not others:
            continue
        n = min(random.randint(min_c, max_c), len(others))
        for post in random.sample(others, k=n):
            tasks.append((user, post))

    success, errors = 0, 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(do_comment, u, p) for u, p in tasks]
        done = 0
        for future in as_completed(futures):
            if future.result():
                success += 1
            else:
                errors += 1
            done += 1
            if done % 100 == 0:
                print(f"  Processed {done}/{len(tasks)}")
    print(f"  Done. {success} comments added, {errors} errors.")
    return success, errors


def do_follow(user, target):
    try:
        headers = {"Authorization": f"Bearer {user['token']}"}
        resp = session.post(f"{BASE_URL}/users/{target['id']}/follow", headers=headers, timeout=TIMEOUT)
        return resp.status_code in (200, 201, 204)
    except Exception:
        return False


def add_follows_parallel(users: list, min_f=3, max_f=10):
    print("\n=== Adding follows (parallel) ===")
    tasks = []
    for user in users:
        others = [u for u in users if u["id"] != user["id"]]
        if not others:
            continue
        n = min(random.randint(min_f, max_f), len(others))
        for target in random.sample(others, k=n):
            tasks.append((user, target))

    success, errors = 0, 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(do_follow, u, t) for u, t in tasks]
        done = 0
        for future in as_completed(futures):
            if future.result():
                success += 1
            else:
                errors += 1
            done += 1
            if done % 100 == 0:
                print(f"  Processed {done}/{len(tasks)}")
    print(f"  Done. {success} follows added, {errors} errors.")
    return success, errors


def main():
    print("Starting hardened seed bot...")
    print(f"Target: {BASE_URL}")

    users = create_users_parallel(100)
    if not users:
        print("No users created, aborting.")
        return

    topic_ids = get_topic_ids()
    posts = create_posts_parallel(users, topic_ids, posts_per_user=2)

    like_count, like_errors = add_likes_parallel(users, posts)
    comment_count, comment_errors = add_comments_parallel(users, posts)
    follow_count, follow_errors = add_follows_parallel(users)

    print("\n" + "=" * 40)
    print("SEED SUMMARY")
    print("=" * 40)
    print(f"Users created:    {len(users)}")
    print(f"Posts created:    {len(posts)}")
    print(f"Likes added:      {like_count} (errors: {like_errors})")
    print(f"Comments added:   {comment_count} (errors: {comment_errors})")
    print(f"Follows added:    {follow_count} (errors: {follow_errors})")
    print("=" * 40)


if __name__ == "__main__":
    main()