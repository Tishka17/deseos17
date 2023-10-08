from typing_extensions import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wish import NewWishDTO
from deseos17.domain.models.wish import WishListId, WishId
from deseos17.presentation.interactor_factory import InteractorFactory

wish_router = APIRouter(prefix="/wishes")


class NewWishSchema(BaseModel):
    wishlist_id: WishListId
    text: str


@wish_router.post("/")
def new_wish(
        ioc: Annotated[InteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends()],
        data: NewWishSchema,
) -> WishId:
    with ioc.create_wish(id_provider) as create_wish:
        return create_wish(NewWishDTO(
            wishlist_id=data.wishlist_id,
            text=data.text,
        ))
