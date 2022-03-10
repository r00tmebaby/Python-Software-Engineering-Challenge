from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from core.authentication import logged_user
from core.connect import session

from core.exception_handler import BidNamic_Exception
from models import database
from models.database import Users
from models.requests import SearchTypes, OrderTypes, OrderBy
from models.responses import SearchResponse
from settings.config import INVALID_USER_ID
from fastapi.encoders import jsonable_encoder
router = APIRouter()


@router.get("/search", name="Search", tags=["Search"])
async def search(
        order_by: OrderTypes,
        search_type: SearchTypes,
        sort_by: OrderBy,
        limit: int = 10,
        current_user: Users = Depends(logged_user)
) -> JSONResponse:
    user_data: Users = session.query(database.Users).filter_by(email=current_user.email).first()
    if user_data is not None:

        limit = limit if limit > 0 else 1

        by_alias = f"""
SELECT
	s.search_term,
	c.structure_value,
	count(s.conversion_value) as total_conversion_value,
	count(s.cost) as total_cost,
	s.conversion_value / s.cost as roas
 FROM
	search_terms AS s,
	campaigns AS c
 WHERE s.cost > 0 and s.campaign_id = c.campaign_id
 GROUP BY
	s.search_term,
	c.structure_value,
	roas
 ORDER BY
	{sort_by} {order_by}
	LIMIT {limit};      
"""
        print(by_alias)
        result = session.execute(by_alias).all()

        return jsonable_encoder({"data": result})
    raise BidNamic_Exception(error_code=INVALID_USER_ID, status_code=status.HTTP_400_BAD_REQUEST)

