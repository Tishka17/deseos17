from datetime import timedelta
from typing import TypeVar, Callable

from aiogram import Bot
from fastapi import FastAPI

from deseos17.adapters.auth.telegram_auth import TelegramAuthenticator
from deseos17.adapters.auth.token import JwtTokenProcessor
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.create_wish import wish_router
from deseos17.presentation.web_api.dependencies.config import WebViewConfig
from deseos17.presentation.web_api.get_own_wishlists import wishlist_router
from deseos17.presentation.web_api.login.router import index_router
from .config import load_web_config
from .ioc import IoC


class WebViewConfigProvider:
    def __init__(self, bot_token: str, login_url: str):
        self.token = bot_token
        self.login_url = login_url
        self.bot_name = None

    async def __call__(self) -> WebViewConfig:
        if self.bot_name is None:
            bot = Bot(self.token)
            self.bot_name = (await bot.get_me()).username
        return WebViewConfig(
            login_url=self.login_url,
            bot_name=self.bot_name,
        )


DependencyT = TypeVar("DependencyT")


def singleton(value: DependencyT) -> Callable[[], DependencyT]:
    """Produce save value as a fastapi dependency."""

    def singleton_factory() -> DependencyT:
        return value

    return singleton_factory


def create_app() -> FastAPI:
    app = FastAPI()
    config = load_web_config()
    ioc = IoC(tg_token=config.bot_token)
    web_view_config_provider = WebViewConfigProvider(
        bot_token=config.bot_token,
        login_url=config.login_url,
    )
    token_processor = JwtTokenProcessor(
        secret=config.jwt_secret,
        expires=timedelta(minutes=15),
        algorithm="HS256",
    )
    telegram_authenticator = TelegramAuthenticator(config.bot_token)
    app.dependency_overrides.update({
        InteractorFactory: singleton(ioc),
        JwtTokenProcessor: singleton(token_processor),
        TelegramAuthenticator: singleton(telegram_authenticator),
        WebViewConfig: web_view_config_provider,
    })
    app.include_router(wish_router)
    app.include_router(wishlist_router)
    app.include_router(index_router)
    return app


app = create_app()
