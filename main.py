import asyncio
import os
import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi_utils.tasks import repeat_every
from starlette.staticfiles import StaticFiles

from core.authentication import delete_expired_sessions
from core.connect import add_records

from core.exception_handler import *
from endpoints import (
    auth,
    users,
    default,
    search
)
from settings.config import API, HOST, PORT

route = FastAPI(
    title=API.get("title"),
    description=API.get("description"),
    contact=API.get("contact"),
    version="0.1",
    debug=True,
    root_path_in_servers=True,
    terms_of_service="TODO",
    license_info=API.get("license")
)

route.mount("/static", StaticFiles(directory="static"), name="static")


def custom_openapi():
    if route.openapi_schema:
        return route.openapi_schema
    openapi_schema = get_openapi(
        title="Bidnamic - API Documentation",
        version="1.0",
        license_info={
            "name": "Uvicorn",
            "url": "https://www.uvicorn.org/",
        },
        description=API_DESCRIPTION,
        routes=route.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    route.openapi_schema = openapi_schema
    return route.openapi_schema


route.openapi = custom_openapi
# Exception handlers
route.add_exception_handler(HTTPException, http_exception_handler)

# Add the routers (endpoints)
route.include_router(default.router)  # Not visible -> Redirects to the API documentation

route.include_router(auth.router)
route.include_router(search.router)
route.include_router(users.router)


# Will delete expired sessions
@route.on_event("startup")
@repeat_every(seconds=1)
async def repeater() -> None:
    await delete_expired_sessions()


if __name__ == '__main__':
    # Adding csv records in the database if empty
    asyncio.run(add_records())

    uvicorn.run(
        "main:route",
        host=HOST,
        port=PORT,
        workers=os.cpu_count(),
        reload=True,
        log_config=f"{pathlib.Path(__file__).parent.resolve()}/Settings/server_logs.ini"
    )
