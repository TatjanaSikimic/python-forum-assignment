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
    database.refresh(new_post)

    return new_post


def convert_attachments_to_dict(attachments):
    dict = {}
    for attachment in attachments:
        dict[attachment.id] = attachment.path
    return dict


def get_display_attachments(post_id, database):
    attachments = database.query(Attachment).filter(Attachment.post_id == post_id).all()

    display_attachments = []
    for attachment in attachments:
        display_attachments.append(DisplayAttachment(id=attachment.id, path=attachment.path))

    display_attachments = convert_attachments_to_dict(display_attachments)
    return display_attachments


def get_display_user(user_id, database):
    user = database.query(User).filter(User.id == user_id).first()

    display_user = DisplayUser(username=user.username, avatar=user.avatar, signature=user.signature)

    return display_user


def get_display_post(post_db, database):
    display_attachments = get_display_attachments(post_db.id, database)

    display_user = get_display_user(post_db.user_id, database)

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
        post = await get_post_by_id(post_db, database)
        display_posts.append(post)

    return display_posts


async def get_post_by_id(post, database):
    display_attachments = get_display_attachments(post.id, database)

    display_user = get_display_user(post.user_id, database)

    thread = database.query(Thread).filter(Thread.id == post.thread_id).first()

    display_post = DisplayPostWithThread(thread_title=thread.title,
                                         thread_dt_created=thread.dt_created,
                                         thread_dt_updated=thread.dt_updated,
                                         title=post.title,
                                         content=post.content,
                                         dt_created=post.dt_created,
                                         dt_updated=post.dt_updated,
                                         user=display_user,
                                         attachments=display_attachments)
    return display_post


def delete_attachments(post_id, database):
    attachments = database.query(Attachment).filter(Attachment.post_id == post_id).all()
    for attachment in attachments:
        database.delete(attachment)
    database.commit()


def delete_comments(post_id, database):
    comments = database.query(Comment).filter(Comment.post_id == post_id).all()
    for comment in comments:
        database.delete(comment)
    database.commit()


def delete_post(post, database):
    delete_attachments(post.id, database)

    delete_comments(post.id, database)
    database.delete(post)
    database.commit()


async def update_post(post: PostUpdate, post_db: Post, thread, database):
    for attachment in post.attachments:

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
