from fastapi import APIRouter
from . import helpers, schemas


router = APIRouter()


@router.get('/{id_thread}')
def get_thread_post_listing():
    # List of posts in thread, requires pagination support
    pass


@router.get('/post/{id_post}')
def get_post_by_id():
    pass


@router.post('/{id_thread}')
def create_thread_post():
    pass


@router.put('/{id_thread}')
def update_thread_post():
    # Post can be edited (updated) only by the same user who created it
    pass


@router.delete('/post/{id_post}')
def delete_post_by_id():
    # Post can be deleted only by the same user who created it
    pass
