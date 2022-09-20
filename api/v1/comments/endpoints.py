from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Params, Page, paginate
from sqlalchemy.orm import Session

import db
from db.models import Post, Comment
from . import helpers, schemas
from .schemas import DisplayComment, DisplayCommentWithPost

router = APIRouter()


# TODO: Retrieve all comments that user created
# TODO: Include post information for that specific comment
# TODO: Add configurable pagination
# User needs to be logged in for this endpoint to function
@router.get('/comments/', response_model=Page[DisplayCommentWithPost])
async def get_user_comments(params: Params = Depends(), database: Session = Depends(db.connection.get_db)):
    user_id = 9
    print(user_id)
    comments = await helpers.get_user_comments(user_id, database)
    return paginate(comments, params)


# TODO: Retrieve all comments for post with specific ID
# TODO: Add configurable pagination
@router.get('/comments/{id_post}', response_model=Page[DisplayComment])
async def get_post_comments(id_post: int, params: Params = Depends(),
                            database: Session = Depends(db.connection.get_db)):
    post = database.query(Post).filter(Post.id == id_post).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id_post} does not exist.")

    post_comments = await helpers.get_post_comments(id_post, database)
    return paginate(post_comments, params)


# TODO: Retrieve a comment with specific ID
# It also needs to include a post it is referring to, and thread as well
@router.get('/single/{id_comment}', response_model=schemas.DisplayCommentWithThread)
async def get_comment_by_id(id_comment: int, database: Session = Depends(db.connection.get_db)):
    comment = database.query(Comment).filter(Comment.id == id_comment).first()
    print(comment.id)
    print(comment.post_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id {id_comment} does not exist")
    comment_to_display = await helpers.get_comment_info(comment, database)

    return comment_to_display


# TODO: Create comment for the post with specific ID
@router.post('/comments/{id_post}', status_code=status.HTTP_201_CREATED)
async def create_post_comment(id_post: int,
                              data: schemas.BaseComment,
                              database: Session = Depends(db.connection.get_db)):
    post = database.query(Post).filter(Post.id == id_post).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id_post} does not exist")

    comment_to_create = await helpers.create_comment(data, post, 9,
                                                     database)  # change user_id to be retrieved from current logged user

    return comment_to_create


# TODO: Update comment for the post with specific ID
# Comment can only be updated by the user who created it
@router.put('/comments/{id_comment}', status_code=status.HTTP_200_OK)
def update_post_comment(id_comment: int,
                        data: schemas.CommentUpdate,
                        database: Session = Depends(db.connection.get_db)):
    # dodati provjeru korisnika

    comment = database.query(Comment).filter(Comment.id == id_comment).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id {id_comment} does not exist")

    updated_comment = helpers.update_comment(comment, data, database)
    return updated_comment


# TODO: Update comment for the post with specific ID
# Comment can only be deleted by the user who created it
@router.delete('/comments/{id_comment}', status_code=status.HTTP_200_OK)
def delete_post_comment(id_comment: int, database: Session = Depends(db.connection.get_db)):
    comment = database.query(Comment).filter(Comment.id == id_comment).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id {id_comment} does not exist")
    database.delete(comment)
    database.commit()
