from fastapi import APIRouter
from . import helpers, schemas


router = APIRouter()


# TODO: Retrieve all posts that user created
# TODO: Include thread information for that specific post
# TODO: Add configurable pagination
# User needs to be logged in for this endpoint to function
@router.get('/')
def get_user_posts():
    pass


# TODO: Retrieve all posts for thread with specific ID
# TODO: Add configurable pagination
@router.get('/{id_thread}')
def get_thread_post_listing():
    pass


# TODO: Retrieve a post with specific ID
# It also needs to include a thread it is referring to
@router.get('/post/{id_post}')
def get_post_by_id():
    pass


# TODO: Create post for the thread with specific ID
@router.post('/{id_thread}')
def create_thread_post():
    pass


# TODO: Update post for the thread with specific ID
# Can only be updated by the user who created the post
@router.put('/{id_thread}')
def update_thread_post():
    pass


# TODO: Delete post for the thread with specific ID
# Can only be deleted by the user who created the post
@router.delete('/post/{id_post}')
def delete_post_by_id():
    pass
