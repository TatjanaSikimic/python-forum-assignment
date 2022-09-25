# This file is used to check whether the request is authorized or not
from typing import Optional

from fastapi import Request, HTTPException, status
from fastapi.openapi.models import OAuthFlows
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2
from fastapi.security.utils import get_authorization_scheme_param

# from .jwt import decode_JWT_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials : HTTPAuthorizationCredentials =  await super(JWTBearer,self).__call__(request=request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired token")

    def verify_JWT(JWT_token: str):
        print('verify')
        # try:
        print("JWT:",JWT_token)

        # payload = decode_JWT_token(JWT_token)
        # print(payload)
        # except:
        #     payload = None

        # return True if payload else False

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
        super().__init__(flows=flows,scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("auth_token")
        print("Authorization:", authorization)


        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param


