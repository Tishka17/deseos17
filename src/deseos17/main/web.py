import os
from datetime import timedelta

from fastapi import FastAPI

from deseos17.adapters.token_processor import JwtTokenProcessor
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.login.router import index_router
from deseos17.presentation.web_api.new_wish import wish_router
from deseos17.presentation.web_api.token import TokenProcessor
from .ioc import IoC


def create_app() -> FastAPI:
    app = FastAPI()
    token = os.getenv("BOT_TOKEN")
    ioc = IoC(tg_token=token)

    token_processor = JwtTokenProcessor(
        secret=token,
        expires=timedelta(minutes=15),
        algorithm="HS256",
    )
    app.dependency_overrides[InteractorFactory] = lambda: ioc
    app.dependency_overrides[TokenProcessor] = lambda: token_processor
    app.include_router(wish_router)
    app.include_router(index_router)
    return app


app = create_app()
