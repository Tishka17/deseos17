import asyncio

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from deseos17.presentation.telegram.create_wish import create_wish_dialog
from deseos17.presentation.telegram.get_own_wishlists import (
    own_wishlists_dialog,
)
from deseos17.presentation.telegram.middlewares.id_provider import (
    IdProviderMiddleware
)
from deseos17.presentation.telegram.start import start_router
from deseos17.presentation.telegram.view_wishlist import wishlist_dialog
from .config import load_bot_config, BotConfig
from .ioc import IoC


def get_dispatcher(config: BotConfig) -> Dispatcher:
    ioc = IoC(tg_token=config.bot_token)
    dp = Dispatcher(ioc=ioc)
    dp.update.middleware(IdProviderMiddleware())
    dp.include_router(start_router)
    dp.include_router(create_wish_dialog)
    dp.include_router(own_wishlists_dialog)
    dp.include_router(wishlist_dialog)
    setup_dialogs(dp)
    return dp


def get_dispatcher_preview() -> Dispatcher:
    return get_dispatcher(BotConfig(bot_token="--"))


async def bot_main():
    config = load_bot_config()
    bot = Bot(config.bot_token)

    await get_dispatcher(config).start_polling(bot)


if __name__ == '__main__':
    asyncio.run(bot_main())
