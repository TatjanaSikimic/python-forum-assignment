from typing import Optional

from fastapi import Request, Response, HTTPException, status, Depends
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2
# from datetime import datetime, timedelta
import datetime
from pydantic import ValidationError

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
        print("Authorization:", authorization)

        scheme, param = get_authorization_scheme_param(authorization)
        print("Param:", param)
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
                    print("Deleting cookie...")
                    response.delete_cookie('auth_token')
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Authentication token is expired.")
                user_id: str = decoded_token.get("sub")
                if user_id is None:
                    raise credentials_exception

        except JWTError:
            raise credentials_exception
        if not authorization or scheme.lower() != "bearer":
            if scheme.lower() != "bearer":
                # print("Deleting cookie...")
                response.delete_cookie('auth_token')
            if self.auto_error:

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication token is expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return decoded_token


def decode_JWT_token(token: str):
    # try:
    print("Decode:", token)
    print("Key:", ALGORITHM)
    decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
    print("decoded:", decoded_token)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    return decoded_token if decoded_token['exp'] >= int(current_time.timestamp()) else None

# def verify_token(token: str, credentials_exception):
#     try:
#         print("Token:", token.strip())
#         payload = decode_JWT_token(token)
#         print("Payload:", payload)
#         token_data = None
#         user_id: str = payload.get("sub")
#
#         # token_data = schemas.TokenData(id=user_id)
#         if not payload:
#             print("exception")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         if user_id is None:
#             raise credentials_exception
#         return payload
#     except JWTError:
#         raise credentials_exception
#
#
# oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login/")
#
#
# async def get_current_user(data=Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials.",
#         headers={"WWW=Authenticate": "Bearer"}
#     )
#
#     return verify_token(data, credentials_exception)
