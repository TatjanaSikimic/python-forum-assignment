from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
import db.connection
from . import schemas, validator, services

router = APIRouter()


# TODO: Add mechanism for registration described in README
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(data: schemas.UserRegistration, database: Session = Depends(db.connection.get_db)):
    print("cc")
    user = await validator.verify_username_exists(data.username, database)
    print("aa")

    if user:
        raise HTTPException(
            status_code=400,
            detail=f"User with {data.username} already exists in the system."
        )

    new_user = await services.register_user(data, database)
    print('bbb')
    return new_user


# TODO: Add mechanism for login described in README
@router.post('/login')
def login_user(data: schemas.UserLogin):
    pass


# TODO: Add mechanism for logout described in README
@router.post('/logout')
def logout_user():
    pass
