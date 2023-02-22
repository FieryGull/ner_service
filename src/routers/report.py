from typing import List

from fastapi import Depends, Request, APIRouter
from fastapi.responses import JSONResponse
from spacy import displacy
from spacy.tokens import Doc
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from src.core.deps import get_current_user, authorize_user, templates
from src.core.ner import get_entities_statistic, NLP
from src.db.db_requests import DBCommands
from src.db.models import User, Report
from src.schemas.main import Report as schemaReport

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/", response_model=List[schemaReport])
async def get_reports(current_user: User = Depends(authorize_user),
                      db_connection: DBCommands = Depends(DBCommands)):
    reports = await db_connection.get_all(Report, user_id=str(current_user.id))
    return reports


@router.get("/{report_id}", response_model=schemaReport)
async def get_report(report_id,
                     current_user: User = Depends(authorize_user),
                     db_connection: DBCommands = Depends(DBCommands)):
    report = await db_connection.get(Report, id=report_id, user_id=str(current_user.id))
    return report


@router.get("/{report_id}/html", response_class=HTMLResponse, description="Generate html-report of processed text")
async def get_report_html(report_id,
                          request: Request,
                          current_user: User = Depends(get_current_user),
                          db_connection: DBCommands = Depends(DBCommands)):
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    report = await db_connection.get(Report, id=report_id, user_id=str(current_user.id))
    doc = Doc(NLP.vocab).from_bytes(report.doc)
    report_data = displacy.render(doc, style="ent", minify=True)
    return templates.TemplateResponse("report_template.html", context={"request": request, "report": report_data})


@router.get("/{report_id}/json", response_class=JSONResponse, description="Generate statistic of found entities")
async def get_report_json(report_id,
                          current_user: User = Depends(authorize_user),
                          db_connection: DBCommands = Depends(DBCommands)):
    report = await db_connection.get(Report, id=report_id, user_id=str(current_user.id))
    doc = Doc(NLP.vocab).from_bytes(report.doc)
    report_dict = get_entities_statistic(doc)
    return report_dict
