from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import db
from db.models import Post, Comment
from . import helpers, schemas

router = APIRouter()


# TODO: Retrieve all comments that user created
# TODO: Include post information for that specific comment
# TODO: Add configurable pagination
# User needs to be logged in for this endpoint to function
@router.get('/')
def get_user_comments():
    user_id = 9



# TODO: Retrieve all comments for post with specific ID
# TODO: Add configurable pagination
@router.get('/{id_post}')
def get_post_comments(id_post: int):
    pass


# TODO: Retrieve a comment with specific ID
# It also needs to include a post it is referring to, and thread as well
@router.get('/single/{id_comment}')
def get_post_by_id():
    pass


# TODO: Create comment for the post with specific ID
@router.post('/{id_post}', status_code= status.HTTP_201_CREATED)
def create_post_comment(id_post: int,
                        data: schemas.BaseComment,
                        database: Session = Depends(db.connection.get_db)):

    post = database.query(Post).filter(Post.id == id_post).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id {id_post} does not exist")

    comment_to_create = helpers.create_comment(data,post,9,database) # change user_id to be retrieved from current logged user

    return comment_to_create



# TODO: Update comment for the post with specific ID
# Comment can only be updated by the user who created it
@router.put('/{id_comment}')
def update_post_comment(id_comment: int,
                        data: schemas.CommentUpdate):
    pass


# TODO: Update comment for the post with specific ID
# Comment can only be deleted by the user who created it
@router.delete('/{id_comment}', status_code= status.HTTP_200_OK)
def delete_post_comment(id_comment: int, database: Session = Depends(db.connection.get_db)):
    comment = database.query(Comment).filter(Comment.id == id_comment).first()

    if not comment:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id {id_comment} does not exist")
    database.delete(comment)
