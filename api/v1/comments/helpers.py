# Can be used for any function that needs to be implemented for the endpoints
from api.v1.posts.schemas import DisplayPost
from api.v1.user.schemas import DisplayUser
from api.v1.posts.helpers import get_post_by_id, get_display_post
from schemas import BaseComment, DisplayComment, DisplayCommentWithPost, DisplayCommentWithThread, CommentUpdate
from datetime import datetime
from db.models import Comment, Thread, Post, Attachment, User


def create_comment(comment, post, user_id, database):
    comment_to_create = Comment(title=comment.title,
                                dt_created=datetime.utcnow(),
                                dt_updated=datetime.utcnow(),
                                content=comment.content,
                                user_id=user_id,
                                post_id=post.id)
    database.add(comment_to_create)
    database.commit()
    database.refresh(comment_to_create)

    post.dt_updated = datetime.utcnow()
    database.add(post)
    database.commit()
    database.refresh(post)

    thread = database.query(Thread).filter(Thread.id == post.thread_id).first()
    thread.dt_updated = datetime.utcnow()

    database.add(thread)
    database.commit()
    database.refresh(thread)

    return comment_to_create


def __convert_attachments_to_dict__(attachments):
    dict = {}
    for attachment in attachments:
        dict[attachment.id] = attachment.path
    return dict


async def get_user_comments(user_id, database):
    comments_db = database.query(Comment).filter(Comment.user_id == user_id).all()
    comments_to_display = []
    for comment in comments_db:
        post_db = database.query(Post).filter(Post.id == comment.post_id).first()

        display_post = get_display_post(post_db, database)

        comment_user = __get_display_user__(comment.user_id, database)
        comment_to_display = DisplayCommentWithPost(post=display_post,
                                                    title=comment.title,
                                                    dt_created=comment.dt_created,
                                                    dt_updated=comment.dt_updated,
                                                    user=comment_user,
                                                    content=comment.content)
        comments_to_display.append(comment_to_display)

    return comments_to_display


def __get_display_user__(user_id, database):
    user_db = database.query(User).filter(User.id == user_id).first()

    display_user = DisplayUser(username=user_db.username,
                               avatar=user_db.avatar,
                               signature=user_db.signatue)
    return display_user


async def get_post_comments(post_id, database):
    comments_db = database.query(Comment).filter(Comment.id == post_id).all()

    comments_to_display = []

    for comment in comments_db:
        display_user = __get_display_user__(comment.user_id, database)

        display_comment = DisplayComment(title=comment.title,
                                         dt_created=comment.dt_created,
                                         dt_updated=comment.dt_updated,
                                         user=display_user,
                                         content=comment.content)
        comments_to_display.append(display_comment)

    return comments_to_display


async def get_comment_info(comment_db, database):
    post_db = database.query(Post).filter(Post.id == comment_db.post_id).first()
    post_with_thread = get_post_by_id(post_db.id, database)

    comment_to_display = DisplayCommentWithThread(post_with_thread=post_with_thread,
                                                  title=post_db.title,
                                                  dt_created=post_db.dt_created,
                                                  dt_updated=post_db.dt_updated,
                                                  user=__get_display_user__(comment_db.user_id, database),
                                                  content=post_db.content)
    return comment_to_display

def update_comment(comment_db: Comment, data: CommentUpdate, database):
    for var, value in vars(data).items():
        setattr(comment_db, var, value) if value else None

    comment_db.dt_updated = datetime.utcnow()

    # update corresponding post
    post_db = database.query(Post).filter(Post.id == comment_db.post_id).first()

    post_db.dt_updated = datetime.utcnow()

    thread_db = database.query(Thread).filter(Thread.id == post_db.thread_id).first()

    thread_db.dt_updated = datetime.utcnow()

    return comment_db

