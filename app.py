import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from src.core.deps import templates
from src.db.db_requests import DBCommands, DBManager
from src.routers import auth, tasks, report, root
from src.settings import APP_PORT, APP_HOST

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(report.router)
app.include_router(root.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_message = exc.errors()[0].get('msg')
    if request.url.path in ["/auth/signup", "/auth/login"] and request.method == "POST":
        return templates.TemplateResponse("login.html", context={"request": request, "error": error_message})
    raise exc


@app.on_event("startup")
async def startup():
    db_connection = DBCommands()
    await db_connection.drop_tables()
    await db_connection.create_tables()


@app.on_event("shutdown")
async def shutdown():
    DBManager.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
