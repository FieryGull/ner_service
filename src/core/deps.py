from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError

from src.core.auth import oauth2_scheme
from src import settings
from src.db.db_requests import DBCommands
from src.db.models import User


templates = Jinja2Templates(directory="src/templates")


async def get_current_user(db_conn: DBCommands = Depends(DBCommands),
                           token: str = Depends(oauth2_scheme)) -> Optional[User]:
    """
    Get current user by JWT

    :param db_conn: db connector
    :param token: token oauth2 scheme
    :return: user instance if exist (else None)
    """
    if token is None:
        return
    try:
        payload = jwt.decode(token,
                             settings.JWT_SECRET,
                             algorithms=[settings.ALGORITHM],
                             options={"verify_aud": False},
                             )

        user_id = payload.get("user_id")

        if user_id is None:
            return

    except JWTError:
        return

    user = await db_conn.get(model=User, id=user_id)
    return user


async def authorize_user(user: Optional[User] = Depends(get_current_user)) -> User:
    """
    Auth user in system

    :param user: [Optional] user instance
    :return: auth user if exist (else HTTP 401 exception)
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"}, )
    if user is None:
        raise credentials_exception

    return user
