from typing import Union
from sqlalchemy.orm import Session
import api.middlewares.auth_middleware as middleware
import config
from fastapi import APIRouter, status, Depends

import db
from db.models import User

token_url = config.TOKEN_URL


# async def common_parameters(
#     database: [Session, None] = db.connection.get_db, current_user: User = middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url), limit: int = 100
# ):
#     return {"database": , "skip": skip, "limit": limit}