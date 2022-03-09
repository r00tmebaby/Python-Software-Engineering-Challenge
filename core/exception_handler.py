from fastapi import Request
from starlette.responses import JSONResponse
from settings.config import *

from fastapi import HTTPException


class BidNamic_Exception(HTTPException):
    def __init__(self, error_code, error_info=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_code = error_code
        self.error_info = error_info


async def http_exception_handler(request: Request, exception: HTTPException):
    """ Overrides the standard FastAPI error_handler for custom messages """
    headers = getattr(exception, 'headers', None)
    error_code = getattr(exception, 'error_code', exception.status_code)
    error_info = getattr(exception, 'error_info', None)
    if not error_info:
        error_info = eval(f"ERROR_DESCRIPTIONS_{LANGUAGE}").get(error_code, exception.detail)
    body = {
        'result_code': error_code,
        'error_info': error_info,
        'data': None,
    }
    return JSONResponse(body, headers=headers, status_code=exception.status_code)
