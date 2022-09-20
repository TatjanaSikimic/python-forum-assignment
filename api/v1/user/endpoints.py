from fastapi import APIRouter, status, Depends, HTTPException
from . import helpers, schemas
from sqlalchemy.orm import Session
import db.connection
from db.models import User
from . import helpers


router = APIRouter()


# You can modify these endpoints to your liking, but support avatar update and user signature update
# If the user is not logged in, none of these endpoints should work

# TODO: Avatar add, update, delete functionality using static files, look in fastapi documentation
# TODO: Signature add, update, delete functionality

@router.post('/avatar/{user_id}', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def add_user_avatar(user_id: int, avatar_link, database: Session = Depends(db.connection.get_db)):
    # static image, should be saved, and can be retrieved as link
    if avatar_link is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Given avatar link is an empty string")
    user = database.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist.")

    updated_user = helpers.add_attr("avatar", avatar_link, user, database)

    return updated_user


@router.delete('/avatar/{user_id}', status_code=status.HTTP_200_OK)
def delete_avatar(user_id: int, database: Session = Depends(db.connection.get_db)):
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist.")

    if user.avatar is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no avatar.")

    user_without_avatar = helpers.delete_attr("avatar", user, database)

    return user_without_avatar


@router.post('/signature/{user_id}', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def add_user_signature(user_id: int, signature, database: Session = Depends(db.connection.get_db)):
    if signature is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Given signature is an empty string")
    user = database.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

    updated_user = helpers.add_attr("signature", signature, user, database)

    return updated_user


@router.put('/signature/{user_id}', status_code=status.HTTP_200_OK)
def update_user_signature(user_id: int, signature, database: Session = Depends(db.connection.get_db)):

    user = database.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

    updated_user = helpers.add_attr("signature", signature, user, database)

    return updated_user

@router.delete('/signature/{user_id}', status_code=status.HTTP_200_OK)
def delete_user_signature(user_id: int, database: Session = Depends(db.connection.get_db)):
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

    if user.signature is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no signature.")

    user_with_deleted_signature = helpers.delete_attr("signature", user, database)

    return user_with_deleted_signature


# TODO: Messaging uses RabbitMQ. You can use pika or aio-pika adapter for RabbitMQ, both are included

@router.post('/messaging')
def send_message_to_user():
    # Message is sent to the amqp service, to user queue
    # If user queue not created, create it, user queues should be named user_{id_user}, e.g. user_1123
    pass


@router.get('/messaging')
def receive_messages():
    # Connect to my user queue, get every message that is in queue, and return it here.
    # For additional challenge, you can permanently store them in-memory, redis or something else
    pass
