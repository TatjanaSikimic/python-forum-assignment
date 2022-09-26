# TODO: Add globals for testing, i.e. username and password, for auth, or retrieving token
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api.v1.auth import endpoints as auth_router
from api.v1.user import endpoints as user_router
from api.v1.threads import router as thread_router
from api.v1.posts import router as post_router
from api.v1.comments import router as comment_router

app = FastAPI(title="Python Forum Assignment", version="0.0.1")

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(thread_router)
app.include_router(post_router)
add_pagination(post_router)
app.include_router(comment_router)
add_pagination(comment_router)

thread_1 = {"title": "Food"}
thread_2 = {"title": "Beauty Tips"}
user_1 = {"username": "user1", "password": "User1@123"}
user_2 = {"username": "user5", "password": "User5@123"}
thread_to_search_id = 8
thread_to_delete_id = 19
thread_to_update_id = 14
thread_to_update = {
    "title": "Health",
    "dtCreated": "2022-09-26 01:34:10.401019",
    "dtUpdated": "2022-09-26 01:34:10.401019",
    "userId": 14
}
