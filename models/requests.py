from pydantic import BaseModel


class UserRequest(BaseModel, orm_mode=True):
    name: str = "r00tme"
    surname: str = "r00tme1"
    summary: str = "user"
    email: str = "r00tme@abv.bg"
    password: str = "R00tme123#"

