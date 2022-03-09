import asyncio
import os
import pathlib
from http.client import HTTPException

import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from core.authentication import delete_expired_sessions
from core.connect import add_records
from core.exception_handler import *
from endpoints import (
    auth,
    users,
    default
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

# Exception handlers
route.add_exception_handler(HTTPException, http_exception_handler)

# Add the routers (endpoints)
route.include_router(default.router)  # Not visible -> Redirects to the API documentation
route.include_router(auth.router)
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
