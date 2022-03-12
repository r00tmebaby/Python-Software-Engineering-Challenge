from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/", name="Redirects to docs", include_in_schema=False, tags=["Default"])
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")

