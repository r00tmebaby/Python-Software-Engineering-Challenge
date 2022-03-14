from fastapi import APIRouter, Depends
from sqlalchemy import text
from starlette import status
from starlette.responses import JSONResponse

from core.authentication import logged_user
from core.connect import session

from core.exception_handler import BidNamic_Exception
import sqlalchemy

from models import database
from models.database import Users, Campaigns, SearchItems, AddGroups
from models.requests import SearchTypes, OrderTypes, OrderBy
from models.responses import QueryModel
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/search", name="Search 🟩", tags=["Search"])
async def search(
        order_by: OrderTypes,
        search_type: SearchTypes,
        sort_by: OrderBy,
        limit: int = 10,
        page: int = 1,
        current_user: Users = Depends(logged_user)
) -> JSONResponse:
    user_data: Users = session.query(database.Users).filter_by(email=current_user.email).first()
    if user_data is not None:

        limit = limit if limit > 0 else 10
        page = page if page > 0 else 1

        with session as ses:
            # Querying the campaign
            search_items = ses.query(
                SearchItems.campaign_id,
                SearchItems.search_term,
                sqlalchemy.func.sum(SearchItems.cost).label('total_cost'),
                sqlalchemy.func.sum(SearchItems.conversion_value).label('total_conversion_value'),
                (sqlalchemy.func.sum(SearchItems.conversion_value) / sqlalchemy.func.sum(SearchItems.cost)).label(
                    "roas")
            ) \
                .select_from(SearchItems) \
                .filter(SearchItems.cost > 0, ) \
                .group_by(SearchItems.search_term, SearchItems.campaign_id) \
                .order_by(text(f'{sort_by} {order_by}')) \
                .limit(limit).offset(page * (page + limit))

            result = []
            for found_items in search_items:
                found_items: QueryModel
                switch_table = "Campaigns" if search_type == "structure_value" else "AddGroups"

                # Switching the tables based on search criteria
                search_switch: eval(switch_table) = ses \
                    .query(eval(switch_table)) \
                    .distinct(eval(switch_table).campaign_id) \
                    .filter(found_items.campaign_id == eval(switch_table).campaign_id) \
                    .one()

                # Adding structure value from campaign table
                result.append(
                    [
                        search_switch.structure_value if search_type == "structure_value" else search_switch.alias,
                        found_items.search_term,
                        found_items.total_cost,
                        found_items.total_conversion_value,
                        found_items.roas
                    ]
                )

        return jsonable_encoder({"data": result})
    raise BidNamic_Exception(error_code=ResourceWarning, status_code=status.HTTP_400_BAD_REQUEST)
