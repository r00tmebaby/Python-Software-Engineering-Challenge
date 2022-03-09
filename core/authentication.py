from datetime import datetime, timedelta
from typing import Optional

from starlette import status
from starlette.responses import JSONResponse
from core.connect import *
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from core.exception_handler import BidNamic_Exception
from models.database import Users
from settings.config import *


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="session")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("email")
        if username is None:
            raise BidNamic_Exception(error_code=INVALID_CREDENTIALS, status_code=status.HTTP_401_UNAUTHORIZED)
        token_data = TokenData(username=username)
    except JWTError:
        raise BidNamic_Exception(error_code=INVALID_CREDENTIALS, status_code=status.HTTP_401_UNAUTHORIZED)
    user = session.query(Users).filter(Users.email == token_data.username).first()
    if user is None:
        raise BidNamic_Exception(error_code=INVALID_CREDENTIALS, status_code=status.HTTP_401_UNAUTHORIZED)
    return user


async def logged_user(current_user: Users = Depends(get_current_user)) -> (Users, JSONResponse):
    session_id = session.query(Sessions).filter(Sessions.user_id == current_user.id).first()
    if session_id is not None:
        return current_user
    raise BidNamic_Exception(error_code=INVALID_USER_TOKEN, status_code=status.HTTP_401_UNAUTHORIZED)


async def delete_expired_sessions():
    session.query(Sessions).filter(time.time() >= Sessions.expires_on).delete()
    session.commit()
