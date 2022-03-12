import datetime
import time

import bcrypt
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from settings.config import DEFAULT_DATE_FORMAT


def hash_password(password: str) -> bytes:
    """ Returns hashed password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def make_JSON(data: object) -> JSONResponse:
    """ Create JSON from any data type and format """
    return JSONResponse(jsonable_encoder(data))
