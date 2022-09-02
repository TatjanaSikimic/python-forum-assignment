from fastapi import APIRouter
from . import helpers, schemas


router = APIRouter()


@router.get('/')
def get_threads():
    # List of threads, requires pagination support
    pass


@router.get('/{id_thread}')
def get_thread():
    pass


@router.post('/{id_thread}')
def create_thread():
    pass


@router.put('/{id_thread}')
def update_thread():
    pass


@router.delete('/{id_thread}')
def delete_thread():
    pass
