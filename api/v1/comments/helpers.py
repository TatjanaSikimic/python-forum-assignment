# Can be used for any function that needs to be implemented for the endpoints
from api.v1.user.schemas import DisplayUser
import api.v1.posts.helpers as post_helpers
from .schemas import DisplayComment, DisplayCommentWithPost, DisplayCommentWithThread, CommentUpdate
import datetime
from db.models import Comment, Thread, Post, User


async def create_comment(comment, post, user_id, database):
    comment_to_create = Comment(title=comment.title,
                                dt_created=datetime.datetime.now(datetime.timezone.utc),
                                dt_updated=datetime.datetime.now(datetime.timezone.utc),
                                content=comment.content,
                                user_id=user_id,
                                post_id=post.id)
    database.add(comment_to_create)
    database.commit()
    # database.refresh(comment_to_create)

    post.dt_updated = datetime.datetime.now(datetime.timezone.utc)
    database.add(post)
    database.commit()
    database.refresh(post)

    thread = database.query(Thread).filter(Thread.id == post.thread_id).first()
    thread.dt_updated = datetime.datetime.now(datetime.timezone.utc)

    database.add(thread)
    database.commit()
    database.refresh(thread)

    database.refresh(comment_to_create)
    return comment_to_create


async def get_user_comments(user_id, database):
    comments_db = database.query(Comment).filter(Comment.user_id == user_id).all()
    comments_to_display = []
    for comment in comments_db:
        post_db = database.query(Post).filter(Post.id == comment.post_id).first()

        display_post = post_helpers.get_display_post(post_db, database)

        comment_user = get_display_user(comment.user_id, database)
        comment_to_display = DisplayCommentWithPost(post=display_post,
                                                    title=comment.title,
                                                    dt_created=comment.dt_created,
                                                    dt_updated=comment.dt_updated,
                                                    user=comment_user,
                                                    content=comment.content)
        comments_to_display.append(comment_to_display)

    return comments_to_display


def get_display_user(user_id, database):
    user_db = database.query(User).filter(User.id == user_id).first()

    display_user = DisplayUser(username=user_db.username,
                               avatar=user_db.avatar,
                               signature=user_db.signature)
    return display_user


async def get_post_comments(post_id, database):
    results = database.query(User, Comment) \
        .join(Comment) \
        .where(Comment.post_id == post_id) \
        .values(User.username,
                User.avatar,
                User.signature,
                Comment.title,
                Comment.dt_created,
                Comment.dt_updated,
                Comment.content) \

    comments_to_display = []

    for result in results:
        display_user = DisplayUser(username=result.username,
                                   avatar=result.avatar,
                                   signature=result.signature)
        display_comment = DisplayComment(title=result.title,
                                         dt_created=result.dt_created,
                                         dt_updated=result.dt_updated,
                                         user=display_user,
                                         content=result.content)
        comments_to_display.append(display_comment)

    return comments_to_display


async def get_comment_info(comment_db, database):
    post_db = database.query(Post).filter(Post.id == comment_db.post_id).first()
    post_with_thread = await post_helpers.get_post_by_id(post_db, database)

    user = get_display_user(comment_db.user_id, database)

    comment_to_display = DisplayCommentWithThread(post=post_with_thread,
                                                  title=comment_db.title,
                                                  dt_created=post_db.dt_created,
                                                  dt_updated=post_db.dt_updated,
                                                  user=user,
                                                  content=comment_db.content)
    return comment_to_display


def update_comment(comment_db: Comment, data: CommentUpdate, database):
    for var, value in vars(data).items():
        setattr(comment_db, var, value) if value else None

    comment_db.dt_updated = datetime.datetime.now(datetime.timezone.utc)
    database.commit()

    # update corresponding post
    post_db = database.query(Post).filter(Post.id == comment_db.post_id).first()

    post_db.dt_updated = datetime.datetime.now(datetime.timezone.utc)
    database.commit()
    database.refresh(post_db)

    thread_db = database.query(Thread).filter(Thread.id == post_db.thread_id).first()

    thread_db.dt_updated = datetime.datetime.now(datetime.timezone.utc)
    database.commit()
    database.refresh(thread_db)

    database.refresh(comment_db)
    return comment_db
