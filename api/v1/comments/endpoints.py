from fastapi import APIRouter
from . import helpers, schemas

router = APIRouter()


# TODO: Retrieve all comments that user created
# TODO: Include post information for that specific comment
# TODO: Add configurable pagination
@router.get('/')
def get_user_comments():
    pass


# TODO: Retrieve all comments for post with specific ID
# TODO: Add configurable pagination
@router.get('/{id_post}')
def get_post_comments(id_post: int):
    pass


# TODO: Retrieve a comment with specific ID
@router.get('/single/{id_comment}')
def get_post_by_id():
    pass


# TODO: Create comment for the post with specific ID
@router.post('/{id_post}')
def create_post_comment(id_post: int,
                        data: schemas.BaseComment):
    pass


# TODO: Update comment for the post with specific ID
# Comment can only be updated by the user who created it
@router.put('/{id_comment}')
def update_post_comment(id_comment: int,
                        data: schemas.CommentUpdate):
    pass


# TODO: Update comment for the post with specific ID
# Comment can only be deleted by the user who created it
@router.delete('/{id_comment}')
def delete_post_comment(id_comment: int):
    pass
