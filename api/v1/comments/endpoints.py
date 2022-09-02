from fastapi import APIRouter
from . import helpers, schemas

router = APIRouter()


@router.get('/{id_post}')
def get_post_comments(id_post: int):
    # List of comments in thread, implement pagination
    pass


@router.post('/{id_post}')
def create_post_comment(id_post: int,
                        data: schemas.BaseComment):
    pass


@router.put('/{id_post}')
def update_post_comment(id_post: int,
                        data: schemas.CommentUpdate):
    # Comment can only be updated by the same person who created it
    pass


@router.delete('/{id_comment}')
def delete_post_comment(id_comment: int):
    # Comment can only be deleted by the person who created it
    pass
