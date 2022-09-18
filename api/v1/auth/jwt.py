from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas

SECRET_KEY = "JuIXoB2b8GMXPkaaawlROw6sG4v7uCVUJZVCxbjk42Y24eql7Sqvg2/ggdkmlicSPCmzjczbU3H3uncMDY9NF95eS0S6PFesHOqH7I9sX3daK+9rhLGdWVQNt450O7Ae6HkHfW9hDtOLQKrP2uJb6fNEos4ttYVTioA9PFsiZEzDodOlpjGP52/74R2C6kfllDXEQjd0MTq1ZwBs3NsDLPBYYps9XSL6yhUSLegv2fJxj1JuTijmdhayzuu7j4PK6iqJixXqmx1+ZDUmVbI7cMGs4G+muvWdJ7zSAHZNRktwXoMzBRN5j4csa4tNNpqW2+QPYaBrAzDTSc/bl+j8QQ=="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    created = datetime.utcnow().timestamp()
    created = int(created)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = int(expire.timestamp())

    to_encode.update({"iat": created, "exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        print(user_id)
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW=Authenticate": "Bearer"}
    )
    return verify_token(data, credentials_exception)