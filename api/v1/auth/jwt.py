from jose import  jwt
import datetime
import config


SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.SESSION_EXPIRE


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_JWT(user_id: str):
    created = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    expire_date = int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    payload = {
        "sub": user_id,
        "iat": created,
        "exp": expire_date
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_response(encoded_jwt)





