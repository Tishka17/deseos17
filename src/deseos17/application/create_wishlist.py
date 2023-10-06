from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.interactor import Interactor
from deseos17.application.common.interfaces import (
    Comitter, WishListSaver,
)
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId
from deseos17.domain.services.wishlist import WishListService


class DbGateway(
    Protocol, Comitter, WishListSaver,
):
    pass


@dataclass
class NewWishListDTO:
    user_id: UserId
    title: str


class CreateWishList(Interactor[NewWishListDTO, WishListId]):
    def __init__(
            self,
            db_gateway: DbGateway,
            wishlist_service: WishListService,
    ):
        self.db_gateway = db_gateway
        self.wishlist_service = wishlist_service

    def __call__(self, data: NewWishListDTO) -> WishListId:
        wishlist = self.wishlist_service.create_wishlist(
            user_id=data.user_id, title=data.title,
        )

        self.db_gateway.save_wishlist(wishlist)
        self.db_gateway.commit()
        return wishlist.id
