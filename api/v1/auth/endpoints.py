from fastapi import APIRouter
from . import helpers, schemas


router = APIRouter()


@router.post('/register')
def register_user(data: schemas.UserRegistration):
    pass


@router.post('/login')
def login_user(data: schemas.UserLogin):
    pass


@router.post('/logout')
def logout_user():
    pass
