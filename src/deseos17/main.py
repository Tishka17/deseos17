import asyncio
import os
from functools import partial

from aiogram import Bot, Dispatcher

from deseos17.adapters.database.fake_db import FakeGateway
from deseos17.application.create_wish.use_case import CreateWish
from deseos17.application.view_wishlist.use_case import ViewWishList
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService
from deseos17.presentation.telegram.new_wish.dialog import new_wish_dialog


def view_wishlist_factory(db_gateway: FakeGateway) -> ViewWishList:
    return ViewWishList(
        db_gateway=db_gateway,
        access_service=AccessService(),
        wish_service=WishService(),
    )


def create_wish_factory(db_gateway: FakeGateway) -> CreateWish:
    return CreateWish(
        db_gateway=db_gateway,
        access_service=AccessService(),
        wish_service=WishService(),
    )


def get_dispatcher():
    dp = Dispatcher()
    db_gateway = FakeGateway()
    dp.include_router(new_wish_dialog(
        view_wishlist_factory=partial(view_wishlist_factory, db_gateway),
        new_wish_factory=partial(create_wish_factory, db_gateway),
    ))
    return dp


async def bot_main():
    token = os.getenv("BOT_TOKEN")
    bot = Bot(token)

    await get_dispatcher().start_polling(bot)


if __name__ == '__main__':
    asyncio.run(bot_main())
