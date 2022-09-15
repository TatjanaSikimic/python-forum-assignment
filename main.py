from fastapi import FastAPI
from api.v1.auth import endpoints as auth_router

app = FastAPI(title="Python Forum Assignment",
              version="0.0.1")

app.include_router(auth_router.router)

# TODO: Include routers
# TODO: Include middleware
# TODO: Include static files handler
# TODO: Include functionality for running app using command: python main.py
