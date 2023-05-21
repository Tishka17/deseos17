from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from deseos17.application.create_wish.dto import NewWishDTO
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId, WishId
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.auth import get_user_id

wish_router = APIRouter(prefix="/wishes")


class NewWishSchema(BaseModel):
    wishlist_id: WishListId
    text: str


@wish_router.post("/")
def new_wish(
        ioc: Annotated[InteractorFactory, Depends()],
        user_id: Annotated[UserId, Depends(get_user_id)],
        data: NewWishSchema,
) -> WishId:
    with ioc.create_wish() as create_wish:
        return create_wish(NewWishDTO(
            user_id=user_id,
            wishlist_id=data.wishlist_id,
            text=data.text,
        ))
