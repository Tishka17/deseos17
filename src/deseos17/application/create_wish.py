from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.transaction import TransactionManager
from deseos17.application.common.wish_gateway import (
    WishListReader, WishSaver, WishListSaver,
    ShareReader,
)
from deseos17.domain.models.wish import WishId, WishListId
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService


class WishDbGateway(
    WishListReader, WishSaver, WishListSaver,
    ShareReader, Protocol,
):
    pass


@dataclass
class NewWishDTO:
    wishlist_id: WishListId
    text: str


class CreateWish(Interactor[NewWishDTO, WishId]):
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

    def __call__(self, data: NewWishDTO) -> WishId:
        user_id = self.id_provider.get_current_user_id()
        wishlist = self.wish_db_gateway.get_wishlist(data.wishlist_id)
        share_rules = self.wish_db_gateway.get_share_rules(wishlist.id, user_id)

        self.access_service.ensure_can_create(wishlist, user_id, share_rules)

        wish = self.wish_service.create_wish(wishlist=wishlist, text=data.text)

        self.wish_db_gateway.save_wish(wish)
        self.wish_db_gateway.save_wishlist(wishlist)
        self.transaction_manager.commit()
        return wish.id
