from typing import Optional

from starlette import status
from typing_extensions import Annotated

from fastapi import APIRouter, Request, Depends, Response, HTTPException
from jinja2 import PackageLoader
from starlette.templating import Jinja2Templates

from deseos17.application.authenticate import LoginResultDTO
from deseos17.domain.exceptions import AuthenticationError
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.token import TokenProcessor

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
        ioc: Annotated[InteractorFactory, Depends()],
        authenticator: Annotated[TokenProcessor, Depends()],
        response: Response,
        fields: Annotated[LoginResultDTO, Depends()],
) -> str:
    with ioc.authenticate() as authenticate:
        try:
            user_id = authenticate(fields)
        except AuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data"
            )
    token = authenticator.create_access_token(user_id)
    response.set_cookie(
        "token", token,
        httponly=True,
    )
    return "ok"
