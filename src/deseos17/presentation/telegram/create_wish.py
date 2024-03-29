from typing import Any, Dict

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Row, Back, Cancel, Next
from aiogram_dialog.widgets.text import Format, Const

from deseos17.application.common.dto import Pagination
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wish import NewWishDTO
from deseos17.application.view_wishlist import ViewWishListDTO
from deseos17.domain.models.wish import WishListId
from deseos17.presentation.interactor_factory import InteractorFactory
from . import states

TEXT_INPUT_ID = "text"


def get_wishlist_id(dialog_manager) -> WishListId:
    return dialog_manager.start_data["wishlist_id"]


async def wishlist_getter(
        dialog_manager: DialogManager,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        **kwargs,
) -> Dict[str, Any]:
    wishlist_id = get_wishlist_id(dialog_manager)
    with ioc.view_wishlist(id_provider) as view_wishlist:
        data = view_wishlist(ViewWishListDTO(
            id=wishlist_id,
            pagination=Pagination(limit=0, offset=0),
        ))
        return {
            "wishlist": data.wishlist,
        }


async def preview_getter(
        dialog_manager: DialogManager, **kwargs,
) -> Dict[str, Any]:
    text: ManagedTextInput = dialog_manager.find(TEXT_INPUT_ID)
    return {
        "text": text.get_value(),
    }


async def on_done(
        event: CallbackQuery, button, dialog_manager: DialogManager,
) -> None:
    text: ManagedTextInput = dialog_manager.find(TEXT_INPUT_ID)
    ioc: InteractorFactory = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]
    with ioc.create_wish(id_provider) as create_wish:
        create_wish(NewWishDTO(
            text=text.get_value(),
            wishlist_id=get_wishlist_id(dialog_manager),
        ))


create_wish_dialog = Dialog(
    Window(
        Format(
            "You are going to add wish into list `{wishlist.title}`.\n"
            "Please, provide text:"
        ),
        Cancel(),
        TextInput(id=TEXT_INPUT_ID, on_success=Next()),
        preview_add_transitions=[
            Next(),
        ],
        getter=wishlist_getter,
        state=states.CreateWish.text,
    ),
    Window(
        Format(
            "You are going to add wish into list `{wishlist.title}`.\n"
            "Your text is: \n{text}\n\n"
            "Please, confirm."
        ),
        Row(
            Button(text=Const("Ok"), id="ok", on_click=on_done),
            Back(),
            Cancel(),
        ),
        getter=[wishlist_getter, preview_getter],
        state=states.CreateWish.preview,
    ),
)
