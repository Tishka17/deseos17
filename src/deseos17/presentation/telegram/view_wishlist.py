from datetime import datetime

from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import (
    StubScroll, NumberedPager, Group, Select, Column,
)
from aiogram_dialog.widgets.text import Const, Format

from deseos17.application.common.dto import Pagination
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.view_wishlist import ViewWishListDTO
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishList, WishListId, Wish, WishId
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.telegram.states import ViewWishList

PAGE_SIZE = 10


async def own_wishlists_getter(
        dialog_manager: DialogManager,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        **kwargs,
):
    wishlist_id = WishListId(dialog_manager.start_data["wishlist_id"])

    scroll: ManagedScroll = dialog_manager.find("scroll")
    page = await scroll.get_page()
    offset = page * PAGE_SIZE

    with ioc.view_wishlist(id_provider) as view_wishlist_interactor:
        data = view_wishlist_interactor(ViewWishListDTO(
            id=wishlist_id,
            pagination=Pagination(
                limit=PAGE_SIZE,
                offset=offset
            )
        ))

    return {
        "total_wishes": data.total_wishes,
        "pages": data.total_wishes // PAGE_SIZE + bool(data.total_wishes % PAGE_SIZE),
        "wishes": data.wishes,
        "wishlist": data.wishlist,
    }


wishlist_dialog = Dialog(
    Window(
        Format("{wishlist.title}\n"),
        Format("Total wishes: {total_wishes} ", when=F["total_wishes"]),
        Const("No wishes", when=~F["total_wishes"]),
        Format("Updated: {wishlist.updated_at}"),
        StubScroll(id="scroll", pages=F["pages"]),
        Column(
            Select(
                Format("{item.text}"),
                item_id_getter=lambda item: item.id,
                type_factory=int,
                items="wishes",
                id="list",
            ),
        ),
        Group(
            NumberedPager(id="pager", scroll="scroll"),
            width=8,
        ),
        getter=own_wishlists_getter,
        preview_data={
            "total_wishes": 4,
            "pages": 2,
            "wishlist": WishList(WishListId(1), UserId(1), title="Listo Uno",
                                 updated_at=datetime.min),
            "wishes": [
                Wish(
                    wishlist_id=WishListId(1), text="Wish 1",
                    updated_at=datetime.min, id=WishId(1),
                ),
                Wish(
                    wishlist_id=WishListId(1), text="Wish 2",
                    updated_at=datetime.min, id=WishId(2),
                ),
                Wish(
                    wishlist_id=WishListId(1), text="Wish 3",
                    updated_at=datetime.min, id=WishId(3),
                ),
                Wish(
                    wishlist_id=WishListId(1), text="Wish 4",
                    updated_at=datetime.min, id=WishId(4),
                ),
            ],
        },
        state=ViewWishList.view,
    )
)
