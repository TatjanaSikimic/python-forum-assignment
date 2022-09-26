from datetime import datetime
from api.v1.user.schemas import DisplayUser
from api.base.schemas import BaseModel


class Thread(BaseModel):
    ### thread class used for uptades
    title: str
    dt_created: str
    dt_updated: str
    user_id: int


class CreateThread(BaseModel):
    title: str


class DisplayThread(BaseModel):
    title: str
    dt_created: datetime
    dt_updated: datetime
    user: DisplayUser
