from typing import Optional

from fastapi import Request, Response, HTTPException, status, Depends
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from fastapi.security import OAuth2
import datetime

from config import config

SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.SESSION_EXPIRE


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: str = None,
            scopes: dict = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request, response: Response) -> Optional[str]:
        authorization: str = request.cookies.get("auth_token")


        scheme, param = get_authorization_scheme_param(authorization)

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW=Authenticate": "Bearer"}
        )
        decoded_token = None

        try:
            if param:
                decoded_token = decode_JWT_token(param)
                if not decoded_token:
                    response.delete_cookie('auth_token')
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Authentication token is expired.")
                user_id: str = decoded_token.get("sub")
                if user_id is None:
                    raise credentials_exception
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Not authenticated")

        except JWTError:
            raise credentials_exception

        return decoded_token


def decode_JWT_token(token: str):
    decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    return decoded_token if decoded_token['exp'] >= int(current_time.timestamp()) else None