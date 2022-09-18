from typing import Optional

from api.base.schemas import BaseModel
from . import validator
from pydantic import validator
from . import validator as pass_validator
class UserRegistration(BaseModel):
    username: str
    password: str

    @validator('password')
    def check_password_strength(cls, v):
        if not pass_validator.check_password_strength(v):
            raise ValueError('Entered password is weak!')
        return v
    pass  # Contains username and password


class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TokenData(BaseModel):
    id: Optional[str] = None
