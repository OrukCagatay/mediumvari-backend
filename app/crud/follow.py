from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.follow import Follow
from app.models.user import User



def follow_user(
    db: Session,
    follower_id: int,
    following_id: int
):
    db_follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )

    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)

    return db_follow



def unfollow_user(
    db: Session,
    follow: Follow
):
    db.delete(follow)
    db.commit()



def get_follow(
    db: Session,        # bu tek bir follow u döner amaç service de daha önce kontrol ediyomu tekrar takip edememesi için var 
    follower_id: int,
    following_id: int
):
    stmt = (
        select(Follow)
        .where(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id
        )
    )

    return db.scalar(stmt)



def get_followers(          ## followers listesi --birini takip edenlerin listesi herkes messiyi takip ediyo
    db: Session,
    user_id: int
):
    stmt = (
        select(User)
        .join(
            Follow,
            User.id == Follow.follower_id
        )
        .where(
            Follow.following_id == user_id
        )
    )

    return db.scalars(stmt).all()




def get_following(      ## bu da birinin takip listesi -- messi kimleri takip ediyo 
    db: Session,
    user_id: int
):
    stmt = (
        select(User)
        .join(
            Follow,
            User.id == Follow.following_id
        )
        .where(
            Follow.follower_id == user_id
        )
    )

    return db.scalars(stmt).all()



def followers_count(
    db: Session,
    user_id: int
):
    stmt = (
        select(func.count())        # takipci sayısı döner 
        .select_from(Follow)
        .where(Follow.following_id == user_id)
    )

    return db.scalar(stmt)



def following_count(
    db: Session,
    user_id: int
):
    stmt = (
        select(func.count())        # takip edilen sayısı 
        .select_from(Follow)
        .where(Follow.follower_id == user_id)
    )

    return db.scalar(stmt)