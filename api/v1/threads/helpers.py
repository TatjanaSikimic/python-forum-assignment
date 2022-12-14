from api.v1.threads.schemas import DisplayThread
from db.models import Thread, User, Post
import datetime
from . import schemas
from ..user.schemas import DisplayUser


async def add_new_thread(data, current_user_id, database):
    date_created = date_updated = datetime.datetime.now(datetime.timezone.utc)  # datetime.utcnow()
    new_thread = Thread(title=data.title, dt_created=date_created, dt_updated=date_updated, user_id=current_user_id)

    database.add(new_thread)
    database.commit()
    database.refresh(new_thread)
    return new_thread


def get_all_threads(database):
    display_threads = []
    results = (database.query(User)
               .with_entities(User.username,
                              User.avatar,
                              User.signature,
                              Thread.title,
                              Thread.dt_created,
                              Thread.dt_updated)
               .join(Thread))

    for thread in results:
        user = DisplayUser(username=thread.username,
                           avatar=thread.avatar,
                           signature=thread.signature)
        display_threads.append(DisplayThread(title=thread.title,
                                             dt_created=thread.dt_created,
                                             dt_updated=thread.dt_updated,
                                             user=user))

    return display_threads


def update_thread(thread: schemas.Thread, db_thread: Thread, database):
    for var, value in vars(thread).items():
        setattr(db_thread, var, value) if value else None
    db_thread.dt_updated = datetime.datetime.now(datetime.timezone.utc)
    database.add(db_thread)
    database.commit()
    database.refresh(db_thread)

    return db_thread


def delete_thread(thread, database):
    posts = database.query(Post).filter(Post.thread_id == thread.id).all()
    for post in posts:
        database.delete(post)
    database.commit()

    database.delete(thread)
    database.commit()
