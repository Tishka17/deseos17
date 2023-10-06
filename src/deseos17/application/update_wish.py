from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.interactor import Interactor
from deseos17.application.common.interfaces import (
    Comitter, WishReader, WishListReader, WishSaver, WishListSaver,
    ShareReader,
)
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import Wish, WishList
from deseos17.domain.models.wish import WishId
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService


@dataclass
class UpdateWishDTO:
    user_id: UserId
    id: WishId
    text: str


class DbGateway(
    Protocol, Comitter, WishReader, WishListReader, WishSaver, WishListSaver,
    ShareReader,
):
    pass


class UpdateWish(Interactor[UpdateWishDTO, None]):
    def __init__(
            self,
            db_gateway: DbGateway,
            access_service: AccessService,
            wish_service: WishService,
    ):
        self.db_gateway = db_gateway
        self.access_service = access_service
        self.wish_service = wish_service

    def __call__(self, data: UpdateWishDTO) -> None:
        wish: Wish = self.db_gateway.get_wish(data.id)
        wishlist: WishList = self.db_gateway.get_wishlist(wish.wishlist_id)
        share_rules = self.db_gateway.get_share_rules(
            wishlist.id, data.user_id,
        )

        self.access_service.ensure_can_edit(
            wishlist, data.user_id, share_rules
        )

        self.wish_service.update_wish(wish, wishlist, new_text=data.text)

        self.db_gateway.save_wish(wish)
        self.db_gateway.save_wishlist(wishlist)
        self.db_gateway.commit()
