from typing import List, Dict
from datetime import datetime

from pydantic import Field
from api.v1.user.schemas import DisplayUser
from api.base.schemas import BaseModel

class Attachment(BaseModel):
    path: str
class PostCreate(BaseModel):
    title: str
    content: str = Field(min_length=50)
    attachments: List[str] = []

class DisplayAttachment(BaseModel):
    id: int
    path: str
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DisplayPost(BaseModel):
    title: str
    dt_created: datetime
    dt_updated: datetime
    user: DisplayUser
    content: str
    attachments: Dict[int,str]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DisplayPostWithTread(BaseModel):
    thread_title: str
    thread_dt_created: datetime
    thread_dt_updated: datetime
    title: str
    dt_created: datetime
    dt_updated: datetime
    user: DisplayUser
    content: str
    attachments: Dict[int,str]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)