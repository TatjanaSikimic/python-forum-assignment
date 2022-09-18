from db.models import User
from . import validator


async def register_user(data, database) -> User:
    hashed_password = validator.get_password_hash(data.password)

    new_user = User(username=data.username, password=hashed_password)

    database.add(new_user)

    database.commit()

    database.refresh(new_user)

    return new_user
