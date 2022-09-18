from api.base.schemas import BaseModel
from pydantic import validator

class DisplayUser(BaseModel):
    ### How user will be displayed in Post/Threads response
    username: str
    avatar: str | None
    signature: str | None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class User(BaseModel):
    username: str
    password: str
    name: str | None
    avatar: str
    signature: str | None
