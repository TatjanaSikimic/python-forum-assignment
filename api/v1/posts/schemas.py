from typing import List, Dict, Union
from datetime import datetime

from pydantic import Field
from api.v1.user.schemas import DisplayUser
from api.base.schemas import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class Attachment(BaseModel):
    path: str


class PostCreate(PostBase):
    attachments: List[str]


class DisplayAttachment(BaseModel):
    id: int
    path: str
    # +


class DisplayPost(PostBase):
    dt_created: datetime
    dt_updated: datetime
    user: DisplayUser
    attachments: Dict[int, str]
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)


class DisplayPostWithThread(DisplayPost):
    thread_title: str
    thread_dt_created: datetime
    thread_dt_updated: datetime
    # title: str
    # dt_created: datetime
    # dt_updated: datetime
    # user: DisplayUser
    # content: str
    # attachments: Dict[int,str]
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)


class AttachmentUpdate(BaseModel):
    id: int
    path: str
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)


class PostUpdate(PostBase):
    # thread_title: str
    # thread_dt_created: datetime
    # thread_dt_updated: datetime
    id: int
    attachments: Union[List[AttachmentUpdate], None] = None
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
