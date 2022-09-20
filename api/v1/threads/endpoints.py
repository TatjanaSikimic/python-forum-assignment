from typing import List

from . import helpers
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.connection
from db.models import Thread, User
from .schemas import DisplayThread
from ..auth.schemas import TokenData
from ..auth.jwt import get_current_user
from . import schemas

router = APIRouter()


# TODO: Retrieve all threads that exist in the application
@router.get('/', response_model=List[DisplayThread])
def get_threads(database: Session = Depends(db.connection.get_db)):
    return helpers.get_all_threads(database)


# TODO: Retrieve single thread by ID
@router.get('/{id_thread}', response_model=DisplayThread)
def get_thread(id_thread: int, database: Session = Depends(db.connection.get_db)):
    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Thread with id {id_thread} doesn't exist")

    user = database.query(User).filter(User.id == thread.user_id).first()

    return DisplayThread(title=thread.title, dt_created=thread.dt_created, dt_updated=thread.dt_updated, user=user)


# TODO: Create thread
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_thread(data: schemas.CreateThread, database: Session = Depends(db.connection.get_db)):
    if data.title is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty title not allowed!")

    thread = await helpers.add_new_thread(data, 9, database)
    return thread


# TODO: Update thread, can only be updated by the user who created it
@router.put('/{id_thread}', status_code=status.HTTP_200_OK)
def update_thread(id_thread: int, data: schemas.Thread, database: Session = Depends(db.connection.get_db)):
    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Thread with id {id_thread} doesn't exist")
    # In case someone sends the non-existent user id
    user = database.query(User).filter(User.id == thread.user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {thread.user_id} doesn't exist")

    updated_thread = helpers.update_thread(data, thread, database)

    return updated_thread


# TODO: Delete thread, can only be deleted by the user who created it
@router.delete('/{id_thread}', status_code=status.HTTP_200_OK)
def delete_thread(id_thread: int, database: Session = Depends(db.connection.get_db)):
    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Thread with id {id_thread} doesn't exist")

    helpers.delete_thread(thread, database)
