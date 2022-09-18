from api.v1.threads.schemas import DisplayThread
from db.models import Thread, User
from datetime import datetime
from . import schemas


async def add_new_thread(data, current_user_id, database):
    ### dodati autorizaciju za sve funkcije
    date_created = date_updated = datetime.utcnow()
    new_thread = Thread(title=data.title, dt_created=date_created, dt_updated=date_updated, user_id=current_user_id)

    database.add(new_thread)
    database.commit()
    database.refresh(new_thread)
    return new_thread


# async def get_thread(thread,database):
#     # print('aaaaa')
#     # results = (database.query(User)
#     #            .join(Thread, Thread.user_id == User.id)
#     #            .values(Thread.title,
#     #                    Thread.dt_created,
#     #                    Thread.dt_updated,
#     #                    User.username,
#     #                    User.avatar,
#     #                    User.signature))
#     user = database.query()
#     user = ThreadUser(username=results['username'],avatar=results['avatar'],signature=results['signature'])
#     thread = DisplayThread(title=results['title'],dt_created=results['dt_created'],dt_updated=results['dt_updated'],user=user)
#     return thread

def get_all_threads(database):
    threads = database.query(Thread).all()
    display_threads = []
    for thread in threads:
        user = database.query(User).filter(User.id == thread.user_id).first()
        display_threads.append(DisplayThread(title=thread.title,
                                             dt_created=thread.dt_created,
                                             dt_updated=thread.dt_updated,
                                             user=user))
    return display_threads


def update_thread(thread: schemas.Thread, db_thread: Thread, database):
    for var, value in vars(thread).items():
        setattr(db_thread, var, value) if value else None
    database.add(db_thread)
    database.commit()
    database.refresh(db_thread)

    return db_thread
