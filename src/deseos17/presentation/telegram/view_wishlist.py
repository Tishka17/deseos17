from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import (
    StubScroll, NumberedPager, Group, Select, Column, Button, Start, Back,
    Cancel,
)
from aiogram_dialog.widgets.text import Const, Format

from deseos17.application.common.dto import Pagination
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.view_wishlist import ViewWishListDTO
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishList, WishListId, Wish, WishId
from deseos17.presentation.interactor_factory import InteractorFactory
from . import states

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
        "pages": data.total_wishes // PAGE_SIZE + bool(
            data.total_wishes % PAGE_SIZE),
        "wishes": data.wishes,
        "wishlist": data.wishlist,
    }


async def add_new_wish(
        event: CallbackQuery, button: Button, dialog_manager: DialogManager,
) -> None:
    await states.start_create_wish(
        dialog_manager=dialog_manager,
        wishlist_id=dialog_manager.start_data["wishlist_id"],
    )


wishlist_dialog = Dialog(
    Window(
        Format("{wishlist.title}\n"),
        Format("Total wishes: {total_wishes} ", when=F["total_wishes"]),
        Const("No wishes", when=~F["total_wishes"]),
        Format("Updated: {wishlist.updated_at}"),
        StubScroll(id="scroll", pages=F["pages"]),
        Button(
            Const("➕ New wish"),
            on_click=add_new_wish,
            id="new",
        ),
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
        Cancel(Const("⬅️ Back")),
        getter=own_wishlists_getter,
        preview_data={
            "total_wishes": 40,
            "pages": 5,
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
            ],
        },
        preview_add_transitions=[
            Start(Const("0"), state=states.CreateWish.text, id="0")
        ],
        state=states.ViewWishList.view,
    )
)
