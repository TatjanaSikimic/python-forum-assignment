# Can be used for any function that needs to be implemented for the endpoints
from schemas import BaseComment
from datetime import datetime
from db.models import Comment, Thread


def create_comment(comment,post,user_id,database):

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



