from typing import Dict

from api.base.schemas import BaseModel
from datetime import datetime

from api.v1.posts.schemas import DisplayPost, DisplayPostWithThread
from api.v1.user.schemas import DisplayUser


class BaseComment(BaseModel):
    title: str  # Needs to have text
    content: str


class CommentUpdate(BaseComment):
    pass


class DisplayComment(BaseComment):
    dt_created: datetime
    dt_updated: datetime
    user: DisplayUser


class DisplayCommentWithPost(DisplayComment):
    post: DisplayPost

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)


class DisplayCommentWithThread(DisplayComment):
    post: DisplayPostWithThread
