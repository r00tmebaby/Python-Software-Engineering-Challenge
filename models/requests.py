from pydantic import BaseModel
from enum import Enum


class UserRequest(BaseModel, orm_mode=True):
    name: str = "r00tme"
    surname: str = "r00tme1"
    summary: str = "user"
    email: str = "r00tme@abv.bg"
    password: str = "R00tme123#"


class OrderTypes(str, Enum):
    DESC = "DESC"
    ASC = "ASC"


class SearchTypes(str, Enum):
    STRUCTURE_VALUE = "structure_value"
    ALIAS = "alias"


class OrderBy(str, Enum):
    ROAS = "roas"


class SearchBy(BaseModel, orm_mode=True):
    type: SearchTypes = "structure_value"
    sort_by: OrderTypes = "DESC"
    order_by: OrderBy = "roas"
    limit: int = 10
