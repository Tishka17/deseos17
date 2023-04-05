from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.input.text import ManagedTextInputAdapter
from aiogram_dialog.widgets.kbd import Button, Row, Back, Cancel, Next
from aiogram_dialog.widgets.text import Format, Const

from deseos17.application.common.use_case import UseCaseFactory
from deseos17.application.create_wish.dto import NewWishDTO
from deseos17.application.create_wish.use_case import CreateWish
from deseos17.application.view_wishlist.use_case import ViewWishList
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId
from .. import states

TEXT_INPUT_ID = "text"


class NewWishController:
    def __init__(
            self,
            view_wishlist_factory: UseCaseFactory[ViewWishList],
            new_wish_factory: UseCaseFactory[CreateWish],
    ):
        self.view_wishlist_factory = view_wishlist_factory
        self.new_wish_factory = new_wish_factory

    def get_wishlist_id(self, dialog_manager) -> WishListId:
        return dialog_manager.start_data["wishlist_id"]

    def wishlist_getter(
            self, dialog_manager: DialogManager, **kwargs,
    ) -> dict[str, Any]:
        view_wishlist = self.view_wishlist_factory()
        wishlist = view_wishlist(self.get_wishlist_id(dialog_manager))
        return {
            "wishlist": wishlist,
        }

    def preview_getter(
            self, dialog_manager: DialogManager, **kwargs,
    ) -> dict[str, Any]:
        text: ManagedTextInputAdapter = dialog_manager.find(TEXT_INPUT_ID)
        return {
            "text": text.get_value(),
        }

    async def on_done(
            self, event: CallbackQuery, button, dialog_manager: DialogManager,
    ) -> None:
        text: ManagedTextInputAdapter = dialog_manager.find(TEXT_INPUT_ID)
        new_wishlist = self.new_wish_factory()
        new_wishlist(NewWishDTO(
            text=text.get_value(),
            wishlist_id=self.get_wishlist_id(dialog_manager),
            user_id=UserId(event.from_user.id),
        ))


def input_text_window(controller: NewWishController) -> Window:
    return Window(
        Format(
            "You are going to add wish into list `{wishlist.name}`.\n"
            "Please, provide text:"
        ),
        TextInput(id=TEXT_INPUT_ID, on_success=Next()),
        getter=controller.wishlist_getter,
        state=states.NewWish.text,
    )


def done_window(controller: NewWishController) -> Window:
    return Window(
        Format(
            "You are going to add wish into list `{wishlist.name}`.\n"
            "Your text is: \n{text}\n\n"
            "Please, confirm."
        ),
        Row(
            Button(text=Const("Ok"), id="ok", on_click=controller.on_done),
            Back(),
            Cancel()
        ),
        getter=[controller.wishlist_getter, controller.preview_getter],
        state=states.NewWish.preview,
    )


def new_wish_dialog(
        view_wishlist_factory: UseCaseFactory[ViewWishList],
        new_wish_factory: UseCaseFactory[CreateWish],
):
    controller = NewWishController(
        view_wishlist_factory, new_wish_factory,
    )
    return Dialog(
        input_text_window(controller),
        done_window(controller),
    )
