from datetime import datetime
from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import (
    StubScroll, NumberedPager, Group, Select, Column, Start,
)
from aiogram_dialog.widgets.text import Const, Format

from deseos17.application.common.dto import Pagination
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.get_own_wishlists import GetOwnWishListsDTO
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishList, WishListId
from deseos17.presentation.interactor_factory import InteractorFactory
from . import states

PAGE_SIZE = 10


async def own_wishlists_getter(
        dialog_manager: DialogManager,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        **kwargs,
):
    scroll: ManagedScroll = dialog_manager.find("scroll")
    page = await scroll.get_page()
    offset = page * PAGE_SIZE

    with ioc.get_own_wishlists(id_provider) as get_own_wishlists_interactor:
        data = get_own_wishlists_interactor(GetOwnWishListsDTO(
            pagination=Pagination(
                limit=PAGE_SIZE,
                offset=offset
            )
        ))

    return {
        "total": data.total,
        "pages": data.total // PAGE_SIZE + bool(data.total % PAGE_SIZE),
        "wishlists": data.wishlists,
    }


async def on_selected(
        event: CallbackQuery, select: Any, dialog_manager: DialogManager,
        wishlist_id: WishListId,
) -> None:
    await states.start_view_wishlist(dialog_manager, wishlist_id)


own_wishlists_dialog = Dialog(
    Window(
        Format("You have {total} wishlists. Select one to view",
               when=F["total"]),
        Const("You have no wishlists.", when=~F["total"]),
        StubScroll(id="scroll", pages=F["pages"]),
        Start(
            Const("➕ New wishlist"),
            state=states.CreateWishList.text,
            id="new",
        ),
        Column(
            Select(
                Format("{item.title}"),
                item_id_getter=lambda item: item.id,
                type_factory=lambda x: WishListId(int(x)),
                items="wishlists",
                on_click=on_selected,
                id="list",
            ),
        ),
        Group(
            NumberedPager(id="pager", scroll="scroll"),
            width=8,
        ),
        getter=own_wishlists_getter,
        preview_data={
            "total": 4,
            "pages": 2,
            "wishlists": [
                WishList(WishListId(1), UserId(1), title="Listo Uno",
                         updated_at=datetime.min),
                WishList(WishListId(2), UserId(1), title="Listo Dos",
                         updated_at=datetime.min),
                WishList(WishListId(3), UserId(1), title="Listo Tres",
                         updated_at=datetime.min),
            ],
        },
        preview_add_transitions=[
            Start(Const("0"), state=states.ViewWishList.view, id="0")
        ],
        state=states.GetOwnWishlists.view,
    )
)
