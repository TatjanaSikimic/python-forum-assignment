from typing import List

from fastapi import APIRouter, status, Depends, HTTPException

import config
from . import helpers, schemas
from sqlalchemy.orm import Session
import db.connection
from db.models import User
from . import helpers
from .schemas import ReceiveMessage
from rabbit_mq.pika_client_service import get_pika_client
# from ..auth.jwt import get_current_user
import api.middlewares.auth_middleware as middleware


router = APIRouter()
token_url = config.TOKEN_URL

# You can modify these endpoints to your liking, but support avatar update and user signature update
# If the user is not logged in, none of these endpoints should work

# TODO: Avatar add, update, delete functionality using static files, look in fastapi documentation
# TODO: Signature add, update, delete functionality

@router.post('/avatar/{user_id}', response_model=schemas.User, status_code=status.HTTP_201_CREATED, )
def add_user_avatar(user_id: int, avatar_link, database: Session = Depends(db.connection.get_db),\
                    current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    # static image, should be saved, and can be retrieved as link
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not allowed to add the avatar.")

    user = database.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist.")


    if avatar_link is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Given avatar link is an empty string")


    updated_user = helpers.add_attr("avatar", avatar_link, user, database)

    return updated_user


@router.delete('/avatar/{user_id}', status_code=status.HTTP_200_OK)
def delete_avatar(user_id: int, database: Session = Depends(db.connection.get_db),
                  current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not allowed to delete the avatar.")

    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist.")

    if user.avatar is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no avatar.")

    user_without_avatar = helpers.delete_attr("avatar", user, database)

    return user_without_avatar


@router.post('/signature/{user_id}', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def add_user_signature(user_id: int, signature,
                       database: Session = Depends(db.connection.get_db),
                       current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not allowed to add the signature.")

    user = database.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")


    if signature is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Given signature is an empty string")


    updated_user = helpers.add_attr("signature", signature, user, database)

    return updated_user


@router.put('/signature/{user_id}', status_code=status.HTTP_200_OK)
def update_user_signature(user_id: int, signature, database: Session = Depends(db.connection.get_db),
                          current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not allowed to change the signature.")

    user = database.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

    updated_user = helpers.add_attr("signature", signature, user, database)

    return updated_user


@router.delete('/signature/{user_id}', status_code=status.HTTP_200_OK)
def delete_user_signature(user_id: int,
                          database: Session = Depends(db.connection.get_db),
                          current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    if current_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not allowed to delete the signature.")

    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

    if user.signature is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no signature.")

    user_with_deleted_signature = helpers.delete_attr("signature", user, database)

    return user_with_deleted_signature


# TODO: Messaging uses RabbitMQ. You can use pika or aio-pika adapter for RabbitMQ, both are included

@router.post('/messaging', status_code=status.HTTP_201_CREATED)
async def send_message_to_user(data: schemas.SendMessage, database: Session = Depends(db.connection.get_db),\
                               current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    # Message is sent to the amqp service, to user queue
    # If user queue not created, create it, user queues should be named user_{id_user}, e.g. user_1123
    current_user_id = int(current_user['sub'])
    print(current_user_id)

    user = database.query(User).filter(User.id == data.user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {user.id} does not exist.")
    message_to_send = helpers.prepare_message_for_sending(data.content, current_user_id, database)
    pika_client = get_pika_client(f"user_{user.id}")
    pika_client.send_message(message_to_send.dict())
    return "Message sent."


@router.get('/messaging', response_model=List[ReceiveMessage])
async def receive_messages(current_user: User = Depends(middleware.OAuth2PasswordBearerWithCookie(tokenUrl=token_url))):
    # Connect to my user queue, get every message that is in queue, and return it here.
    # For additional challenge, you can permanently store them in-memory, redis or something else
    current_user_id = int(current_user['sub'])
    print(current_user_id)
    pika_client = get_pika_client(f"user_{current_user_id}")
    messages = pika_client.receive_message()
    # for message in messages:
    #     print(message)
    messages_to_receive = helpers.prepare_messages_for_receiving(messages)
    return messages_to_receive
