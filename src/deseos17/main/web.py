from fastapi import FastAPI

from .ioc import IoC
from ..presentation.interactor_factory import InteractorFactory
from ..presentation.web_api.new_wish import wish_router


def create_app():
    app = FastAPI()
    ioc = IoC()
    app.dependency_overrides[InteractorFactory] = lambda: ioc
    app.include_router(wish_router)
    return app


app = create_app()
