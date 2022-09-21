import json
import datetime
from db.models import Post, Thread, Attachment, User, Comment
from .schemas import DisplayPost, DisplayAttachment, DisplayPostWithThread, PostUpdate
from api.v1.user.schemas import DisplayUser


async def create_post(post, user_id, thread, database):
    date_created = date_updated = datetime.datetime.now(datetime.timezone.utc)
    new_post = Post(title=post.title,
                    dt_created=date_created,
                    dt_updated=date_updated,
                    user_id=user_id,
                    content=post.content,
                    thread_id=thread.id)
    database.add(new_post)
    database.flush()
    database.refresh(new_post)

    attachments = post.attachments
    for attachment in attachments:
        new_attachment = Attachment(path=attachment, post_id=new_post.id)
        database.add(new_attachment)
        database.commit()
        database.refresh(new_attachment)

    ### Update the dt_updated in thread
    thread.dt_updated = date_updated
    database.add(thread)
    database.commit()
    database.refresh(thread)
    print(new_post)
    database.refresh(new_post)

    return new_post


def __convert_attachments_to_dict__(attachments):
    dict = {}
    for attachment in attachments:
        dict[attachment.id] = attachment.path
    return dict


def __get_display_attachments__(post_id, database):
    attachments = database.query(Attachment).filter(Attachment.post_id == post_id).all()

    display_attachments = []
    for attachment in attachments:
        display_attachments.append(DisplayAttachment(id=attachment.id, path=attachment.path))

    display_attachments = __convert_attachments_to_dict__(display_attachments)
    return display_attachments


def __get_display_user__(user_id, database):
    user = database.query(User).filter(User.id == user_id).first()

    display_user = DisplayUser(username=user.username, avatar=user.avatar, signature=user.signature)

    return display_user


def get_display_post(post_db, database):
    display_attachments = __get_display_attachments__(post_db.id, database)

    display_user = __get_display_user__(post_db.user_id, database)

    display_post = DisplayPost(title=post_db.title,
                               dt_created=post_db.dt_created,
                               dt_updated=post_db.dt_updated,
                               user=display_user,
                               content=post_db.content,
                               attachments=display_attachments)
    return display_post


async def get_posts_by_thread(thread_id, database):
    display_posts = []
    posts_db = database.query(Post).filter(Post.thread_id == thread_id).all()

    for post_db in posts_db:
        post = get_display_post(post_db, database)
        display_posts.append(post)

    return display_posts


async def get_posts_by_user(user_id, database):
    display_posts = []
    posts_db = database.query(Post).filter(Post.user_id == user_id).all()

    for post_db in posts_db:
        print(post_db)
        post = await get_post_by_id(post_db, database)
        display_posts.append(post)

    return display_posts


async def get_post_by_id(post, database):
    print("aa")
    display_attachments = __get_display_attachments__(post.id, database)

    display_user = __get_display_user__(post.user_id, database)

    thread = database.query(Thread).filter(Thread.id == post.thread_id).first()
    print(post.title)

    display_post = DisplayPostWithThread(thread_title=thread.title,
                                         thread_dt_created=thread.dt_created,
                                         thread_dt_updated=thread.dt_updated,
                                         title=post.title,
                                         content=post.content,
                                         dt_created=post.dt_created,
                                         dt_updated=post.dt_updated,
                                         user=display_user,
                                         attachments=display_attachments)
    print(display_post)
    return display_post


def __delete_attachments__(post_id, database):
    attachments = database.query(Attachment).filter(Attachment.post_id == post_id).all()
    [database.delete(attachment) for attachment in attachments]
    database.commit()


def __delete_comments__(post_id, database):
    comments = database.query(Comment).filter(Comment.post_id == post_id).all()
    [database.delete(comment) for comment in comments]
    database.commit()


def delete_post(post, database):
    __delete_attachments__(post.id, database)

    __delete_comments__(post.id, database)
    database.delete(post)
    database.commit()


async def update_post(post: PostUpdate, post_db: Post, thread, database):
    # for key in post.attachments:
    #     attachment_to_update = Attachment(path=post.attachments[key])
    #     database.add(attachment_to_update)
    #     database.commit()
    #     database.refresh(attachment_to_update)

    for attachment in post.attachments:
        print(attachment.id)

        if attachment.id > 0:
            attachment_to_update = database.query(Attachment).filter(Attachment.id == attachment.id).first()
            attachment_to_update.path = attachment.path
        else:
            attachment_to_update = Attachment(path=attachment.path,
                                              post_id=post_db.id)
        database.add(attachment_to_update)
        database.commit()
        database.refresh(attachment_to_update)

    post_db.title = post.title
    post_db.content = post.content
    post_db.dt_updated = datetime.datetime.now(datetime.timezone.utc)

    database.add(post_db)
    database.commit()
    database.refresh(post_db)

    thread.dt_updated = datetime.datetime.now(datetime.timezone.utc)
    database.add(thread)
    database.commit()
    database.refresh(thread)
    database.refresh(post_db)
    return post_db
