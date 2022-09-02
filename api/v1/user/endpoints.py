from fastapi import APIRouter
from . import helpers, schemas


router = APIRouter()


# You can modify these endpoints to your liking, but support avatar update and user signature update
# If the user is not logged in, none of these endpoints should work

# TODO: Avatar add, update, delete functionality using static files, look in fastapi documentation
# TODO: Signature add, update, delete functionality

@router.post('/avatar')
def add_user_avatar():
    # static image, should be saved, and can be retrieved as link
    pass


@router.delete('/avatar')
def delete_avatar():
    pass


@router.post('/signature')
def add_user_signature():
    pass


@router.put('/signature')
def update_user_signature():
    pass


@router.delete('/signature')
def delete_user_signature():
    pass


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
