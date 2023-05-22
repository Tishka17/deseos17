from fastapi import FastAPI

from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.login.router import index_router
from deseos17.presentation.web_api.new_wish.router import wish_router
from .ioc import IoC


def create_app() -> FastAPI:
    app = FastAPI()
    ioc = IoC()
    app.dependency_overrides[InteractorFactory] = lambda: ioc
    app.include_router(wish_router)
    app.include_router(index_router)
    return app


app = create_app()
