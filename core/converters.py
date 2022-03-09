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


def date2time(date: str, date_format: str = DEFAULT_DATE_FORMAT) -> float:
    return float(time.mktime(time.strptime(date, date_format)))


def time2date(timestamp, date_format: str = DEFAULT_DATE_FORMAT) -> str:
    timestamp = datetime.datetime.fromtimestamp(float(timestamp))
    return timestamp.strftime(date_format)
