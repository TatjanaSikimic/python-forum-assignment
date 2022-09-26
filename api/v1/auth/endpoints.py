import json

from fastapi import APIRouter, Depends, HTTPException, Response, status, Body, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

import config
import db.connection
from . import schemas, validator, helpers
from db.models import User

from .jwt import sign_JWT
import api.middlewares.auth_middleware as middleware

router = APIRouter()
token_url = config.TOKEN_URL


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(data: schemas.UserRegistration, database: Session = Depends(db.connection.get_db)):
    user = await validator.verify_username_exists(data.username, database)

    if user:
        raise HTTPException(
            status_code=400,
            detail=f"User with {data.username} already exists in the system."
        )

    new_user = await helpers.register_user(data, database)
    return new_user


# TODO: Add mechanism for registration described in README

# TODO: Add mechanism for login described in README

@router.post('/login', status_code=status.HTTP_200_OK)
def login_user(response: Response, request: OAuth2PasswordRequestForm = Depends(),
               database: Session = Depends(db.connection.get_db)):
    user = database.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not validator.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")

    auth_token = sign_JWT(str(user.id))

    response.set_cookie(key="auth_token", value=f"Bearer {auth_token['access_token']}", httponly=True)

    return auth_token


# TODO: Add mechanism for logout described in README
@router.post('/logout', status_code=status.HTTP_200_OK)
def logout_user(response: Response,
                current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    response.delete_cookie(key='auth_token')
    return "User logged out."
