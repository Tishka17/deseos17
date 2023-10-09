from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.interfaces import (
    Comitter, WishListSaver,
)
from deseos17.domain.models.wish import WishListId
from deseos17.domain.services.wishlist import WishListService


class DbGateway(
    Protocol, Comitter, WishListSaver,
):
    pass


@dataclass
class NewWishListDTO:
    title: str


class CreateWishList(Interactor[NewWishListDTO, WishListId]):
    def __init__(
            self,
            db_gateway: DbGateway,
            wishlist_service: WishListService,
            id_provider: IdProvider,
    ):
        self.db_gateway = db_gateway
        self.wishlist_service = wishlist_service
        self.id_provider = id_provider

    def __call__(self, data: NewWishListDTO) -> WishListId:
        user_id = self.id_provider.get_current_user_id()

        wishlist = self.wishlist_service.create_wishlist(
            user_id=user_id, title=data.title,
        )

        self.db_gateway.save_wishlist(wishlist)
        self.db_gateway.commit()
        return wishlist.id
