from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from src import settings
from src.core.security import verify_password
from src.db.db_requests import DBCommands
from src.db.models import User


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(self, tokenUrl: str, scheme_name: str = None, scopes: dict = None, auto_error: bool = True):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(header_authorization)
        cookie_scheme, cookie_param = get_authorization_scheme_param(cookie_authorization)

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param
        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param
        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl=settings.TOKEN_URL, auto_error=False)


async def authenticate(email: str, password: str, db_conn: DBCommands) -> Optional[User]:
    """
    Authenticate user by credentials

    :param email: user's email
    :param password: user's password
    :param db_conn: db connector
    :return: user instance if exist (else None)
    """
    user = await db_conn.get(model=User, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(user_id: str) -> str:
    """
    Create access token for auth

    :param user_id: will correspond to the user ID
    :return: hash token
    """
    return _create_token(token_type="access_token",
                         lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                         user_id=user_id,
                         )


def _create_token(token_type: str, lifetime: timedelta, user_id: str) -> str:
    """
    Construct JWT token and encode it

    :param token_type: token_type
    :param lifetime: token lifetime in minutes
    :param user_id: user id
    :return: hash token
    """
    payload = {}
    expire = datetime.utcnow() + lifetime  # expiration time
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["user_id"] = user_id

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
