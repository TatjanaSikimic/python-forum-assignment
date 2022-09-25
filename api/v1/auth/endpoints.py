import json

from fastapi import APIRouter, Depends, HTTPException, Response, status, Body, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

import db.connection
from . import schemas, validator, helpers
from db.models import User

from .jwt import sign_JWT, create_access_token, get_current_user
from .jwt_bearer import JWTBearer
from .schemas import TokenData, UserLogin
from api.middlewares.auth_middleware import add_process_time_header

router = APIRouter()


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
# @router.get('/me')
# async def get_me(dependencies=Depends(JWTBearer())):
#     print((dependencies))
#     JWTBearer.verify_JWT(JWT_token=dependencies)
#
#     return "ok"

@router.get('/me')
async def get_me(current_user: User = Depends(get_current_user)):
    print(current_user)
    print(current_user['sub'])
    return "ok"


@router.post('/login')
def login_user(response: Response, request: OAuth2PasswordRequestForm = Depends(),
               database: Session = Depends(db.connection.get_db)):
    user = database.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not validator.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")

    auth_token = sign_JWT(str(user.id))
    print(auth_token)
    response.set_cookie(key="auth_token", value=f"Bearer {auth_token['access_token']}", httponly=True)
    print(response.body)
    return auth_token


# @router.post('/login')
# def login_user(request: UserLogin = Body(default=None), database: Session = Depends(db.connection.get_db)):
#     user = database.query(User).filter(User.username == request.username).first()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
#
#     if not validator.verify_password(request.password, user.password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")
#
#     return sign_JWT(str(user.id))


# TODO: Add mechanism for logout described in README
@router.post('/logout')
def logout_user(response: Response, current_user: User = Depends(get_current_user)):
    print('logging out')
    response.delete_cookie(key='auth_token')
    return "User logged out."
