from fastapi import APIRouter
from . import helpers, schemas


router = APIRouter()


# TODO: Add mechanism for registration described in README
@router.post('/register')
def register_user(data: schemas.UserRegistration):
    pass


# TODO: Add mechanism for login described in README
@router.post('/login')
def login_user(data: schemas.UserLogin):
    pass


# TODO: Add mechanism for logout described in README
@router.post('/logout')
def logout_user():
    pass
