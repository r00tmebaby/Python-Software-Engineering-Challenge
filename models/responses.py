from pydantic import BaseModel
from typing import List, Any


class Pagination(BaseModel):
    """Wraps the response so that it returns only limited number of results"""

    page: int = 2
    pages: int = 2
    records: int = 2
    limit: int = 2
    has_more: bool = False
    data: List[Any] = []


class User(BaseModel):
    name: str


class UsersList(BaseModel):
    """ Will return information about all users"""

    total_users: int
    pages: int
    per_page: int
    current_page: int
    has_more: bool
    data: List[User]


class SearchResponse(BaseModel):
    total_users: int
    pages: int
    per_page: int
    current_page: int
    has_more: bool
    data: List[User]