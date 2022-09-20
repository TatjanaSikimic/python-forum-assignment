from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api.v1.auth import endpoints as auth_router
from api.v1.user import endpoints as user_router
from api.v1.threads import router as thread_router
from api.v1.posts import router as post_router
from api.v1.comments import router as comment_router

from api.v1.auth.jwt import get_current_user

app = FastAPI(title="Python Forum Assignment",
              version="0.0.1")

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(thread_router)
app.include_router(post_router)
add_pagination(post_router)
app.include_router(comment_router)
add_pagination(comment_router)

# TODO: Include routers
# TODO: Include middleware
# TODO: Include static files handler
# TODO: Include functionality for running app using command: python main.py
