from typing import List

import config
from . import helpers
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.connection
from db.models import Thread, User
from .schemas import DisplayThread
# from ..auth.jwt import get_current_user
# from api.middlewares.auth_middleware import get_current_user
import api.middlewares.auth_middleware as middleware
from ..auth.schemas import TokenData

from . import schemas

router = APIRouter()

token_url = config.TOKEN_URL


# TODO: Retrieve all threads that exist in the application
@router.get('/', response_model=List[DisplayThread], status_code=status.HTTP_200_OK)
def get_threads(database: Session = Depends(db.connection.get_db)):
    return helpers.get_all_threads(database)


# TODO: Retrieve single thread by ID
@router.get('/{id_thread}', response_model=DisplayThread, status_code=status.HTTP_200_OK)
def get_thread(id_thread: int, database: Session = Depends(db.connection.get_db)):
    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Thread with id {id_thread} doesn't exist")

    user = database.query(User).filter(User.id == thread.user_id).first()

    return DisplayThread(title=thread.title, dt_created=thread.dt_created, dt_updated=thread.dt_updated, user=user)


# TODO: Create thread
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_thread(data: schemas.CreateThread,
                        database: Session = Depends(db.connection.get_db),
                        current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    if data.title is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty title not allowed!")
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    thread = await helpers.add_new_thread(data, current_user_id, database)
    return thread


# TODO: Update thread, can only be updated by the user who created it
@router.put('/{id_thread}', status_code=status.HTTP_200_OK)
def update_thread(id_thread: int, data: schemas.Thread, database: Session = Depends(db.connection.get_db),
                  current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Thread with id {id_thread} doesn't exist")

    if current_user_id != thread.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Thread can only be updated by the user who created it")
    # In case someone sends the non-existent user id
    user = database.query(User).filter(User.id == thread.user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {thread.user_id} doesn't exist")

    updated_thread = helpers.update_thread(data, thread, database)

    return updated_thread


# TODO: Delete thread, can only be deleted by the user who created it
@router.delete('/{id_thread}', status_code=status.HTTP_200_OK)
def delete_thread(id_thread: int,
                  database: Session = Depends(db.connection.get_db),
                  current_user=Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Thread with id {id_thread} doesn't exist")

    if thread.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Thread can only be deleted by the user who created it")

    helpers.delete_thread(thread, database)
