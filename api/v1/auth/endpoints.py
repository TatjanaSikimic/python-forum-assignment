from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import db.connection
from . import schemas, validator, services
from db.models import User
from .jwt import create_access_token
router = APIRouter()


# TODO: Add mechanism for registration described in README
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(data: schemas.UserRegistration, database: Session = Depends(db.connection.get_db)):
    user = await validator.verify_username_exists(data.username, database)

    if user:
        raise HTTPException(
            status_code=400,
            detail=f"User with {data.username} already exists in the system."
        )

    new_user = await services.register_user(data, database)
    return new_user


# TODO: Add mechanism for login described in README
@router.post('/login')
def login_user(request: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(db.connection.get_db)):
    user = database.query(User).filter(User.username == request.username).first()

    if not User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not validator.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")

    #Generate a JWT token
    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


# TODO: Add mechanism for logout described in README
@router.post('/logout')
def logout_user():
    pass
