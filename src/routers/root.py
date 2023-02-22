from fastapi import Depends, Request, APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from src.core.deps import get_current_user, templates
from src.db.db_requests import DBCommands
from src.db.models import User, Report

router = APIRouter(
    tags=["root"]
)


@router.get("/")
async def root(request: Request,
               current_user: User = Depends(get_current_user),
               db_connection: DBCommands = Depends()):
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    reports = await db_connection.get_all(Report, user_id=str(current_user.id))
    return templates.TemplateResponse("home.html", context={"request": request, "reports": reports})
