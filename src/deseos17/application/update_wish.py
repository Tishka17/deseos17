from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.transaction import TransactionManager
from deseos17.application.common.wish_gateway import (
    WishReader, WishListReader, WishSaver, WishListSaver,
    ShareReader,
)
from deseos17.domain.models.wish import Wish, WishId
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService


@dataclass
class UpdateWishDTO:
    id: WishId
    text: str


class WishDbGateway(
    WishReader, WishListReader, WishSaver, WishListSaver,
    ShareReader, Protocol,
):
    pass


class UpdateWish(Interactor[UpdateWishDTO, None]):
    def __init__(
            self,
            wish_db_gateway: WishDbGateway,
            access_service: AccessService,
            wish_service: WishService,
            id_provider: IdProvider,
            transaction_manager: TransactionManager,
    ):
        self.wish_db_gateway = wish_db_gateway
        self.access_service = access_service
        self.wish_service = wish_service
        self.id_provider = id_provider
        self.transaction_manager = transaction_manager

    def __call__(self, data: UpdateWishDTO) -> None:
        user_id = self.id_provider.get_current_user_id()
        wish: Wish = self.wish_db_gateway.get_wish(data.id)
        wishlist = self.wish_db_gateway.get_wishlist(wish.wishlist_id)
        share_rules = self.wish_db_gateway.get_share_rules(
            wishlist.id, user_id,
        )

        self.access_service.ensure_can_edit(wishlist, user_id, share_rules)

        self.wish_service.update_wish(wish, wishlist, new_text=data.text)

        self.wish_db_gateway.save_wish(wish)
        self.wish_db_gateway.save_wishlist(wishlist)
        self.transaction_manager.commit()
