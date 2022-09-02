from fastapi import APIRouter
from . import helpers, schemas


router = APIRouter()


# TODO: Retrieve all threads that exist in the application
@router.get('/')
def get_threads():
    pass


# TODO: Retrieve single thread by ID
@router.get('/{id_thread}')
def get_thread():
    pass


# TODO: Create thread
@router.post('/')
def create_thread():
    pass


# TODO: Update thread, can only be updated by the user who created it
@router.put('/{id_thread}')
def update_thread():
    pass


# TODO: Delete thread, can only be deleted by the user who created it
@router.delete('/{id_thread}')
def delete_thread():
    pass
