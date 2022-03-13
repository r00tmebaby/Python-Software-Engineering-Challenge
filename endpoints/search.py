import dataclasses

from fastapi import APIRouter, Depends
from pydantic import BaseModel
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
from settings.config import INVALID_USER_ID
from fastapi.encoders import jsonable_encoder

router = APIRouter()


class QueryModel(BaseModel):
    campaign_id: int
    search_term: str
    total_cost: float
    total_conversion_value: float
    roas: float


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
                .filter(SearchItems.cost > 0) \
                .group_by(SearchItems.search_term, SearchItems.campaign_id) \
                .order_by(text(f'{sort_by} {order_by}')) \
                .limit(limit).offset(page * (page + limit))

            test = []
            for found_items in search_items:
                found_items: QueryModel

                if search_type == "structure_value":
                    # Querying the campaign table and remove any (campaign_id) duplicates
                    search_switch: Campaigns = ses \
                        .query(Campaigns) \
                        .distinct(Campaigns.campaign_id) \
                        .filter(found_items.campaign_id == Campaigns.campaign_id) \
                        .one()
                else:

                    # Querying the adgroups table and remove any (campaign_id) duplicates
                    search_switch: AddGroups = ses \
                        .query(AddGroups) \
                        .distinct(AddGroups.campaign_id) \
                        .filter(found_items.campaign_id == AddGroups.campaign_id) \
                        .one()

                # Adding structure value from campaign table
                test.append(
                    [
                        search_switch.structure_value if search_type == "structure_value" else search_switch.alias,
                        found_items.search_term,
                        found_items.total_cost,
                        found_items.total_conversion_value,
                        found_items.roas
                    ]
                )

        return jsonable_encoder({"data": test})
    raise BidNamic_Exception(error_code=INVALID_USER_ID, status_code=status.HTTP_400_BAD_REQUEST)

