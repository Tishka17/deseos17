from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import DialogManager

from deseos17.domain.models.wish import WishListId


class CreateWish(StatesGroup):
    text = State()
    preview = State()


class CreateWishList(StatesGroup):
    text = State()
    preview = State()


class GetOwnWishlists(StatesGroup):
    view = State()


class ViewWishList(StatesGroup):
    view = State()


async def start_create_wish(
        dialog_manager: DialogManager, wishlist_id: WishListId,
):
    await dialog_manager.start(
        CreateWish.text,
        data={"wishlist_id": wishlist_id},
    )


async def start_view_wishlist(
        dialog_manager: DialogManager, wishlist_id: WishListId,
):
    await dialog_manager.start(
        ViewWishList.view,
        data={"wishlist_id": wishlist_id},
    )
