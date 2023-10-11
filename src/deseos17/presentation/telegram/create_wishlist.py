from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Row, Cancel, Next, Start
from aiogram_dialog.widgets.text import Format, Const

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wishlist import NewWishListDTO
from deseos17.presentation.interactor_factory import InteractorFactory
from . import states

TEXT_INPUT_ID = "text"


async def preview_getter(
        dialog_manager: DialogManager, **kwargs,
) -> Dict[str, Any]:
    text: ManagedTextInput = dialog_manager.find(TEXT_INPUT_ID)
    return {
        "title": text.get_value(),
    }


async def on_done(
        event: CallbackQuery, button, dialog_manager: DialogManager,
) -> None:
    text: ManagedTextInput = dialog_manager.find(TEXT_INPUT_ID)
    ioc: InteractorFactory = dialog_manager.middleware_data["ioc"]
    id_provider: IdProvider = dialog_manager.middleware_data["id_provider"]
    with ioc.create_wishlist(id_provider) as create_wishlist_interactor:
        wishlist_id = create_wishlist_interactor(NewWishListDTO(
            title=text.get_value(),
        ))
    await states.start_view_wishlist(dialog_manager, wishlist_id)


async def on_view_closed(
        start_data: Data, result: Any, dialog_manager: DialogManager,
):
    await dialog_manager.done()


create_wishlist_dialog = Dialog(
    Window(
        Format(
            "You are going to create a new wishlist.\n\n"
            "Please, provide title:"
        ),
        Cancel(),
        TextInput(id=TEXT_INPUT_ID, on_success=Next()),
        preview_add_transitions=[
            Next(),
        ],
        state=states.CreateWishList.text,
    ),
    Window(
        Format(
            "You are going to create a new wishlist with title: "
            "{title}\n\n"
            "Please, confirm or provide new title."
        ),
        Row(
            Button(text=Const("Ok"), id="ok", on_click=on_done),
            Cancel()
        ),
        TextInput(id=TEXT_INPUT_ID),
        preview_add_transitions=[
            Start(Const("0"), state=states.ViewWishList.view, id="0"),
        ],
        getter=[preview_getter],
        state=states.CreateWishList.preview,
    ),
    on_process_result=on_view_closed,
)
