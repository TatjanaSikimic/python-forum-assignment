import time

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
# from datetime import datetime, timedelta
import datetime
from pydantic import ValidationError

import config
from . import schemas
from .jwt_bearer import OAuth2PasswordBearerWithCookie
from .schemas import TokenData

SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.SESSION_EXPIRE


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_JWT(user_id: str):
    print("user_id")
    created = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    expire_date = int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    payload = {
        "sub": user_id,
        "iat": created,
        "exp": expire_date
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_response(encoded_jwt)


def decode_JWT_token(token: str):
    # try:
        print("Decode:",token)
        print("Key:",ALGORITHM)
        decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        print("decoded:",decoded_token)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        return decoded_token if decoded_token['exp'] >= int(current_time.timestamp()) else None
    # except:
    #     print("exc")
    #     raise {}


def create_access_token(data: dict):
    to_encode = data.copy()
    print("To encode:", to_encode)
    created = datetime.datetime.now(datetime.timezone.utc)
    created = int(created.timestamp())

    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = int(expire.timestamp())

    to_encode.update({"iat": created, "exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        print("Token:", token.strip())
        payload = decode_JWT_token(token)
        print("Payload:",payload)
        token_data = None
        user_id: str = payload.get("sub")


        # token_data = schemas.TokenData(id=user_id)
        if not payload:
            print("exception")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login/")


async def get_current_user(data = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW=Authenticate": "Bearer"}
    )

    return verify_token(data, credentials_exception)

