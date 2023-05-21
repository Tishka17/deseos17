from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.input.text import ManagedTextInputAdapter
from aiogram_dialog.widgets.kbd import Button, Row, Back, Cancel, Next
from aiogram_dialog.widgets.text import Format, Const

from deseos17.application.create_wish.dto import NewWishDTO
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.telegram import states

TEXT_INPUT_ID = "text"


def get_wishlist_id(dialog_manager) -> WishListId:
    return dialog_manager.start_data["wishlist_id"]


def wishlist_getter(
        dialog_manager: DialogManager,
        ioc: InteractorFactory,
        **kwargs,
) -> dict[str, Any]:
    with ioc.view_wishlist() as view_wishlist:
        wishlist = view_wishlist(get_wishlist_id(dialog_manager))
        return {
            "wishlist": wishlist,
        }


def preview_getter(
        dialog_manager: DialogManager, **kwargs,
) -> dict[str, Any]:
    text: ManagedTextInputAdapter = dialog_manager.find(TEXT_INPUT_ID)
    return {
        "text": text.get_value(),
    }


async def on_done(
        event: CallbackQuery, button, dialog_manager: DialogManager,
) -> None:
    text: ManagedTextInputAdapter = dialog_manager.find(TEXT_INPUT_ID)
    ioc: InteractorFactory = dialog_manager.middleware_data["ioc"]
    with ioc.create_wish() as create_wish:
        create_wish(NewWishDTO(
            text=text.get_value(),
            wishlist_id=get_wishlist_id(dialog_manager),
            user_id=UserId(event.from_user.id),
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
