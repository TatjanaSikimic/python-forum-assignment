from fastapi import APIRouter
from . import helpers, schemas
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.connection
from db.models import Thread, Post, User

from ..auth.schemas import TokenData
from ..auth.jwt import get_current_user
from . import schemas

router = APIRouter()


# TODO: Retrieve all posts that user created
# TODO: Include thread information for that specific post
# TODO: Add configurable pagination
# User needs to be logged in for this endpoint to function
@router.get('/posts/user', response_model=List[schemas.DisplayPostWithTread])
async def get_user_posts(user_id: int, database: Session = Depends(db.connection.get_db)):
    ### dodati limit
    user = database.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"User with id {user_id} does not exist.")

    user_posts = await helpers.get_posts_by_user(user_id,database)
    return user_posts



# TODO: Retrieve all posts for thread with specific ID
# TODO: Add configurable pagination
@router.get('/posts/{id_thread}', response_model=List[schemas.DisplayPost])
async def get_thread_post_listing(id_thread: int, database: Session = Depends(db.connection.get_db)):
    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Thread with id {id_thread} does not exist.")
    print(thread.id)
    posts = await helpers.get_posts_by_thread(id_thread,database)
    return posts


# TODO: Retrieve a post with specific ID
# It also needs to include a thread it is referring to
@router.get('/post/{id_post}', response_model=schemas.DisplayPostWithTread)
async def get_post_by_id(id_post: int, database: Session = Depends(db.connection.get_db)):
    post = database.query(Post).filter(Post.id == id_post).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id_post} does not exist")
    display_post = await helpers.get_post_by_id(post,database)
    return display_post


# TODO: Create post for the thread with specific ID
@router.post('/{id_thread}', status_code=status.HTTP_201_CREATED)
def create_thread_post(id_thread: int, data: schemas.PostCreate, database: Session = Depends(db.connection.get_db)):
    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Thread with id {id_thread} does not exists")
    new_post = helpers.create_post(data, 9, thread, database)

    return new_post


# TODO: Update post for the thread with specific ID
# Can only be updated by the user who created the post
@router.put('/{id_thread}', status_code=status.HTTP_200_OK)
async def update_thread_post(id_thread: int, data: schemas.DisplayPost, database: Session = Depends(db.connection.get_db)):
    thread = database.query(Thread).filter(Thread.id == id_thread).first()

    if not thread:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Thread with id {id_thread} does not exist")
    post_db = database.query(Post).filter(Post.id == data.id).first()

    if not post_db:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {data.id} does not exist")



    helpers.update_post(data,post_db,thread,database)




# TODO: Delete post for the thread with specific ID
# Can only be deleted by the user who created the post
@router.delete('/post/{id_post}')
def delete_post_by_id(id_post: int, database: Session = Depends(db.connection.get_db)):
    post = database.query(Post).filter(Post.id == id_post).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id_post} does not exist")

    helpers.delete_post(post,database)


