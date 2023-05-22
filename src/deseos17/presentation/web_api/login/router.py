from typing import Annotated

from fastapi import APIRouter, Request, Depends, Response
from jinja2 import PackageLoader
from starlette.templating import Jinja2Templates

from deseos17.application.auth.dto import LoginResultDTO
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.auth import HttpAuthenticator

index_router = APIRouter()

jinja_loader = PackageLoader("deseos17.presentation.web_api.login")
templates = Jinja2Templates(directory="templates", loader=jinja_loader)


@index_router.get("/index")
def index(
        request: Request,
):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@index_router.get("/login")
def login(
        request: Request,
        id: int,
        auth_date: int,
        first_name: str,
        username: str,
        photo_url: str,
        hash: str,
        ioc: Annotated[InteractorFactory, Depends()],
        authenticator: Annotated[HttpAuthenticator, Depends()],
        response: Response,
) -> str:
    with ioc.authenticate() as authenticate:
        user_id = authenticate(LoginResultDTO(
            id=id,
            auth_date=auth_date,
            first_name=first_name,
            username=username,
            photo_url=photo_url,
            hash=hash,
        ))
    token = authenticator.create_access_token(user_id)
    response.set_cookie("token", token)
    return "ok"
