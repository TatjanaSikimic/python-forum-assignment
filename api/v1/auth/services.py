from db.models import User
from . import validator

async def register_user(data, database) -> User:
    print('b;a')
    hashed_password = validator.get_password_hash(data.password)
    print(data.username)
    print(data.password)
    new_user = User(username=data.username, password=hashed_password)
    print(database)
    database.add(new_user)
    print('tatjana')
    print(database)
    database.commit()
    print(database)
    print('tatjana1')
    database.refresh(new_user)
    print(database)
    print('tatjana2')

    return new_user