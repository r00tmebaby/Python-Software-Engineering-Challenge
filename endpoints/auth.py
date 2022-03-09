from fastapi import APIRouter, Form
from starlette import status

from core.authentication import *
from core.exception_handler import BidNamic_Exception
from core.validators import *
from core.converters import make_JSON
from models.database import *
from settings.config import *
from core.connect import session

router = APIRouter()


class CustomOAuth2Form:
    def __init__(
            self,
            username: str = Form(...),
            password: str = Form(...),
    ):
        self.username = username
        self.password = password


@router.post(
    path="/session",
    tags=["Authentication"],
    name="Login  🟩",
)
async def login_user(data: CustomOAuth2Form = Depends()) -> JSONResponse:
    if is_valid_email(data.username):
        user: Users = session.query(Users).filter_by(email=data.username).first()
        if user is not None and user.is_password_valid(data.password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"email": user.email}, expires_delta=access_token_expires
            )

            session.query(Sessions).filter(Sessions.user_id == user.id).delete()
            session.commit()
            if session.query(Sessions).filter(Sessions.user_id == user.id).first() is None:
                session.add(
                    Sessions(
                        user_id=user.id,
                        access_token=access_token,
                        created_on=time.time(),
                        expires_on=time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
                    )
                )
                session.commit()
            else:
                raise BidNamic_Exception(error_code=USER_ALREADY_LOGGED, status_code=status.HTTP_400_BAD_REQUEST)
            return make_JSON(
                {
                    "access_token": access_token,
                    "token_type": "bearer"
                }
            )
        else:
            raise BidNamic_Exception(error_code=INVALID_CREDENTIALS, status_code=status.HTTP_401_UNAUTHORIZED)

    else:
        raise BidNamic_Exception(error_code=INVALID_EMAIL, status_code=status.HTTP_400_BAD_REQUEST)


@router.delete(
    path="/session",
    tags=["Authentication"],
    name="Logout  🟩 ",
)
async def logout_user(current_user: Users = Depends(logged_user)):
    if session.query(Sessions).filter(Sessions.user_id == current_user.id).all() is not None:
        session.query(Sessions).filter(Sessions.user_id == current_user.id).delete()
        session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=None)
    raise BidNamic_Exception(error_code=INVALID_USER_TOKEN, status_code=status.HTTP_400_BAD_REQUEST)
