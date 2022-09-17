from typing import Optional

from sqlalchemy.orm import Session

from db.models import User

from passlib.context import CryptContext

import re

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def verify_username_exists(username: str, db_session: Session) -> Optional[User]:
    return db_session.query(User).filter(User.username == username).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def check_password_strength(password=None):
    # return(re.search(r'[0-9]', password) and re.search(r'[A-Z]', password) and re.search(r'[!@#$&*]')
    #  and len(password) >= 8)
    return re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password)