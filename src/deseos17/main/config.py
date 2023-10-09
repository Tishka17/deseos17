import os
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

BOT_TOKEN_ENV = "BOT_TOKEN"
JWT_SECRET_ENV = "JWT_SECRET"


@dataclass
class BotConfig:
    bot_token: str


@dataclass
class WebConfig:
    bot_token: str
    jwt_secret: str


def load_bot_config() -> BotConfig:
    bot_token = os.getenv(BOT_TOKEN_ENV)
    if not bot_token:
        logger.error("%s is not set", BOT_TOKEN_ENV)
    return BotConfig(bot_token=bot_token)


def load_web_config() -> WebConfig:
    bot_token = os.getenv(BOT_TOKEN_ENV)
    if not bot_token:
        logger.error("%s is not set", BOT_TOKEN_ENV)
    jwt_secret = os.getenv(JWT_SECRET_ENV)
    if not jwt_secret:
        logger.error("%s is not set", JWT_SECRET_ENV)
    return WebConfig(bot_token=bot_token, jwt_secret=jwt_secret)
