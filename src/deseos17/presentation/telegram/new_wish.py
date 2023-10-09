from typing import Any, Dict

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.input.text import ManagedTextInputAdapter
from aiogram_dialog.widgets.kbd import Button, Row, Back, Cancel, Next
from aiogram_dialog.widgets.text import Format, Const

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wish import NewWishDTO
from deseos17.application.view_wishlist import ViewWishListDTO
from deseos17.domain.models.wish import WishListId
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.telegram import states

TEXT_INPUT_ID = "text"


def get_wishlist_id(dialog_manager) -> WishListId:
    return dialog_manager.start_data["wishlist_id"]


def wishlist_getter(
        dialog_manager: DialogManager,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        **kwargs,
) -> Dict[str, Any]:
    with ioc.view_wishlist(id_provider) as view_wishlist:
        wishlist_id = get_wishlist_id(dialog_manager)
        wishlist = view_wishlist(ViewWishListDTO(wishlist_id))
        return {
            "wishlist": wishlist,
        }


def preview_getter(
        dialog_manager: DialogManager, **kwargs,
) -> Dict[str, Any]:
    text: ManagedTextInputAdapter = dialog_manager.find(TEXT_INPUT_ID)
    return {
        "text": text.get_value(),
    }


async def on_done(
        event: CallbackQuery, button, dialog_manager: DialogManager,
) -> None:
    text: ManagedTextInputAdapter = dialog_manager.find(TEXT_INPUT_ID)
    ioc: InteractorFactory = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]
    with ioc.create_wish(id_provider) as create_wish:
        create_wish(NewWishDTO(
            text=text.get_value(),
            wishlist_id=get_wishlist_id(dialog_manager),
        ))


new_wish_dialog = Dialog(
    Window(
        Format(
            "You are going to add wish into list `{wishlist.name}`.\n"
            "Please, provide text:"
        ),
        TextInput(id=TEXT_INPUT_ID, on_success=Next()),
        getter=wishlist_getter,
        state=states.NewWish.text,
    ),
    Window(
        Format(
            "You are going to add wish into list `{wishlist.name}`.\n"
            "Your text is: \n{text}\n\n"
            "Please, confirm."
        ),
        Row(
            Button(text=Const("Ok"), id="ok", on_click=on_done),
            Back(),
            Cancel()
        ),
        getter=[wishlist_getter, preview_getter],
        state=states.NewWish.preview,
    ),
)
