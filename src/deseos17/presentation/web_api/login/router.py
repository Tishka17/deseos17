from fastapi import APIRouter, Request, Depends, Response, HTTPException
from jinja2 import PackageLoader
from starlette import status
from starlette.templating import Jinja2Templates
from typing_extensions import Annotated

from deseos17.adapters.auth.telegram_auth import (
    TelegramAuthenticator, TelegramAuthIdProvider,
)
from deseos17.adapters.auth.token import JwtTokenProcessor
from deseos17.application.authenticate import LoginResultDTO
from deseos17.application.common.id_provider import IdProvider
from deseos17.domain.exceptions import AuthenticationError
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.dependencies.config import WebViewConfig
from deseos17.presentation.web_api.dependencies.depends_stub import Stub

index_router = APIRouter()

jinja_loader = PackageLoader("deseos17.presentation.web_api.login")
templates = Jinja2Templates(directory="templates", loader=jinja_loader)


@index_router.get("/index")
def index(
        request: Request,
        view_config: Annotated[WebViewConfig, Depends(Stub(WebViewConfig))],
):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "login_url": view_config.login_url,
            "bot_name": view_config.bot_name,
        }
    )


def telegram_auth_id_provider(
        request: Request,
        hash: str,
        authenticator: Annotated[TelegramAuthenticator, Depends(Stub(TelegramAuthenticator))],
):
    return TelegramAuthIdProvider(
        authenticator=authenticator,
        hash=hash,
        fields=request.query_params,
    )


@index_router.get("/login")
def login(
        ioc: Annotated[InteractorFactory, Depends()],
        token_processor: Annotated[JwtTokenProcessor, Depends()],
        id_provider: Annotated[IdProvider, Depends(telegram_auth_id_provider)],
        response: Response,
        fields: Annotated[LoginResultDTO, Depends()],
) -> str:
    with ioc.authenticate(id_provider) as authenticate:
        try:
            user_id = authenticate(fields)
        except AuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data"
            )
    token = token_processor.create_access_token(user_id)
    response.set_cookie(
        "token", token,
        httponly=True,
    )
    return "ok"
