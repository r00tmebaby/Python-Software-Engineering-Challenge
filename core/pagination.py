import math
from typing import List, Any
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from models.responses import Pagination


def paginate(query: List[Any], page: int, limit: int) -> JSONResponse:
    """
    Return standardized pagination JSON response based on Pagination response model

    Parameters
    -----------

    query: List[Any]
        list of database objects
    page: int
        Currently requested page
    limit: int
        How many objects to be displayed per page
    """

    response = Pagination()
    response.records = len(query)
    response.limit = 10 if response.records <= limit < 0 else limit
    response.pages = (
        1 if response.records == 0 else math.ceil(response.records / response.limit)
    )
    response.page = page if page in range(1, response.pages + 1) else 1
    offset = (response.page - 1) * limit
    response.has_more = response.page < response.pages
    response.data = query[offset: offset + limit]
    return jsonable_encoder(response)
