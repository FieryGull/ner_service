from fastapi import APIRouter
from fastapi import HTTPException, Depends, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status
from starlette.responses import RedirectResponse, JSONResponse

from src.core.auth import authenticate, create_access_token
from src.core.deps import templates, get_current_user
from src.db.db_requests import DBCommands
from src.db.models import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/login")
async def get_login_page(request: Request,
                         current_user: User = Depends(get_current_user)):
    if current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", context={"request": request})


@router.post("/login")
async def user_login(request: Request,
                     form_data: OAuth2PasswordRequestForm = Depends(),
                     db_connection: DBCommands = Depends()):
    user = await authenticate(email=form_data.username,
                              password=form_data.password,
                              db_conn=db_connection)
    if not user:
        return templates.TemplateResponse("login.html", context={"request": request,
                                                                 'error': "Invalid username or password"})

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {create_access_token(user_id=str(user.id))}",
        httponly=True,
    )

    return response


@router.get("/signup")
async def get_signup_page(request: Request,
                          current_user: User = Depends(get_current_user)):
    if current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", context={"request": request})


@router.post("/signup", status_code=201)
async def user_signup(request: Request,
                      email: EmailStr = Form(...),
                      password: str = Form(...),
                      db_connection: DBCommands = Depends()):
    user_instance, is_created = await db_connection.get_or_create_user(email=email,
                                                                       password=password)
    if not is_created:
        return templates.TemplateResponse("login.html", context={"request": request,
                                                                 'error': "The user with this email already exists in "
                                                                          "the system"})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return response


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie("Authorization")
    return response


@router.post("/token", response_class=JSONResponse)
async def token(form_data: OAuth2PasswordRequestForm = Depends(),
                db_connection: DBCommands = Depends()):
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = await authenticate(email=form_data.username,
                              password=form_data.password,
                              db_conn=db_connection)
    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

    return {
        "access_token": create_access_token(user_id=str(user.id)),
        "token_type": "bearer",
    }
