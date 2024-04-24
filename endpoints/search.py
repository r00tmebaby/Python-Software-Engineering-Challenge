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
    current_user: Users = Depends(logged_user),
    db: Session = Depends(get_database_session)
) -> JSONResponse:
    user_data = db.query(Users).filter_by(email=current_user.email).first()
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Adjust the limit and page values
    limit = max(limit, 1)
    offset = (page - 1) * limit

    # Mapping to avoid eval
    table_mapping = {
        "structure_value": Campaigns,
        "add_groups": AddGroups
    }

    # Prepare the base query
    search_items = db.query(
        SearchItems.campaign_id,
        SearchItems.search_term,
        func.sum(SearchItems.cost).label('total_cost'),
        func.sum(SearchItems.conversion_value).label('total_conversion_value'),
        (func.sum(SearchItems.conversion_value) / func.sum(SearchItems.cost)).label("roas")
    ).filter(SearchItems.cost > 0).group_by(
        SearchItems.search_term, SearchItems.campaign_id
    ).order_by(text(f'{sort_by} {order_by}')).limit(limit).offset(offset)

    result = []
    for found_items in search_items:
        target_table = table_mapping.get(search_type)
        search_switch = db.query(target_table).distinct(target_table.campaign_id).filter(
            target_table.campaign_id == found_items.campaign_id
        ).one_or_none()

        if search_switch:
            result.append({
                "structure_value": search_switch.structure_value if search_type == "structure_value" else search_switch.alias,
                "search_term": found_items.search_term,
                "total_cost": found_items.total_cost,
                "total_conversion_value": found_items.total_conversion_value,
                "roas": found_items.roas
            })

    return JSONResponse(content={"data": result})
