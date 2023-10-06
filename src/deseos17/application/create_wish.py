from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.interactor import Interactor
from deseos17.application.common.interfaces import (
    Comitter, WishListReader, WishSaver, WishListSaver,
    ShareReader,
)
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishList, WishId
from deseos17.domain.models.wish import WishListId
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService


class DbGateway(
    Comitter, WishListReader, WishSaver, WishListSaver,
    ShareReader, Protocol,
):
    pass


@dataclass
class NewWishDTO:
    wishlist_id: WishListId
    user_id: UserId
    text: str


class CreateWish(Interactor[NewWishDTO, WishId]):
    def __init__(
            self,
            db_gateway: DbGateway,
            access_service: AccessService,
            wish_service: WishService,
    ):
        self.db_gateway = db_gateway
        self.access_service = access_service
        self.wish_service = wish_service

    def __call__(self, data: NewWishDTO) -> WishId:
        wishlist: WishList = self.db_gateway.get_wishlist(data.wishlist_id)
        share_rules = self.db_gateway.get_share_rules(
            wishlist.id, data.user_id,
        )

        self.access_service.ensure_can_create(
            wishlist, data.user_id, share_rules,
        )

        wish = self.wish_service.create_wish(wishlist=wishlist, text=data.text)

        self.db_gateway.save_wish(wish)
        self.db_gateway.save_wishlist(wishlist)
        self.db_gateway.commit()
        return wish.id
