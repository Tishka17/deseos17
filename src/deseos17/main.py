import asyncio
import os
from contextlib import contextmanager

from aiogram import Bot, Dispatcher

from deseos17.adapters.database.fake_db import FakeGateway
from deseos17.application.create_wish.use_case import CreateWish
from deseos17.application.view_wishlist.use_case import ViewWishList
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.telegram.new_wish.dialog import new_wish_dialog


class IoC(InteractorFactory):
    def __init__(self):
        self.db_gateway = FakeGateway()

    @contextmanager
    def view_wishlist(self) -> ViewWishList:
        yield ViewWishList(
            db_gateway=self.db_gateway,
            access_service=AccessService(),
            wish_service=WishService(),
        )

    @contextmanager
    def create_wish(self) -> CreateWish:
        yield CreateWish(
            db_gateway=self.db_gateway,
            access_service=AccessService(),
            wish_service=WishService(),
        )


def get_dispatcher():
    ioc = IoC()
    dp = Dispatcher(ioc=ioc)
    dp.include_router(new_wish_dialog)
    return dp


async def bot_main():
    token = os.getenv("BOT_TOKEN")
    bot = Bot(token)

    await get_dispatcher().start_polling(bot)


if __name__ == '__main__':
    asyncio.run(bot_main())
