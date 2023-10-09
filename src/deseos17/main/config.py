import os
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

BOT_TOKEN_ENV = "BOT_TOKEN"
JWT_SECRET_ENV = "JWT_SECRET"
LOGIN_URL_ENV = "LOGIN_URL"


class ConfigParseError(ValueError):
    pass


@dataclass
class BotConfig:
    bot_token: str


@dataclass
class WebConfig:
    bot_token: str
    jwt_secret: str
    login_url: str


def get_str_env(key) -> str:
    val = os.getenv(key)
    if not val:
        logger.error("%s is not set", key)
        raise ConfigParseError(f"{key} is not set")
    return val


def load_bot_config() -> BotConfig:
    bot_token = get_str_env(BOT_TOKEN_ENV)
    return BotConfig(bot_token=bot_token)


def load_web_config() -> WebConfig:
    bot_token = get_str_env(BOT_TOKEN_ENV)
    jwt_secret = get_str_env(JWT_SECRET_ENV)
    login_url = get_str_env(LOGIN_URL_ENV)
    return WebConfig(
        bot_token=bot_token,
        jwt_secret=jwt_secret,
        login_url=login_url,
    )
