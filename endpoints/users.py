from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse
from core.authentication import logged_user
from core.exception_handler import BidNamic_Exception
from core.validators import *
from models.database import Users
from models.requests import UserRequest
from models import database
from core.connect import session
from settings.config import *

router = APIRouter()


@router.post("/user", tags=["Users"], name="Registration 🟩 ", response_model=UserRequest)
async def add_new_user(user_data: UserRequest) -> JSONResponse:
    if not bool(session.query(database.Users).filter_by(email=user_data.email).first()):
        if is_valid_email(user_data.email):
            if is_valid_password(user_data.password):
                user = database.Users()
                user.name = user_data.name
                user.email = user_data.email
                user.summary = user_data.summary
                user.surname = user_data.surname
                user.password = Users.password_hash(user_data.password)
                session.add(user)
                try:
                    session.commit()
                    return user
                except ConnectionError:
                    raise BidNamic_Exception(
                        error_code=INVALID_USER_ID,
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                raise BidNamic_Exception(error_code=PASSWORD_INVALID, status_code=status.HTTP_400_BAD_REQUEST)
        else:
            raise BidNamic_Exception(error_code=INVALID_EMAIL, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        raise BidNamic_Exception(error_code=DUPLICATE_EMAIL, status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    path="/user",
    tags=["Users"],
    name="Get Current User Information 🟩",
)
async def get_current_user(current_user: Users = Depends(logged_user)) -> JSONResponse:
    user_data: Users = session.query(database.Users).filter_by(email=current_user.email).first()
    if user_data is not None:
        return JSONResponse(user_data.get_limited_info())
    raise BidNamic_Exception(error_code=INVALID_USER_ID, status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    path="/user/{user_id}",
    tags=["Admin"],
    name="Get User Information by ID 🟩",
    description="* Get limited user information (TBD)"
)
async def get_user_by_id(user_id: int):
    user_data: Users = session.query(database.Users).filter_by(id=user_id).first()
    if user_data is not None:
        return JSONResponse(user_data.get_limited_info())
    raise BidNamic_Exception(error_code=INVALID_USER_ID, status_code=status.HTTP_400_BAD_REQUEST)

