from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from src.core.deps import authorize_user
from src.db.models import User
from src.schemas.main import SourceText as schemaSourceText
from src.worker import process_text, celery

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/", status_code=201)
async def create_task(source_data: schemaSourceText,
                      current_user: User = Depends(authorize_user)
                      ):
    task = process_text.delay(source_data.name, str(current_user.id), source_data.text_data)
    return JSONResponse({"task_id": task.id})


@router.get("/{task_id}")
def get_status(task_id, current_user: User = Depends(authorize_user)):
    task_result = celery.AsyncResult(str(task_id))
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
