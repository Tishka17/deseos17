from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.wish_gateway import (
    WishListReader, ShareReader,
)
from deseos17.domain.models.wish import WishList, WishListId
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService


@dataclass
class ViewWishListDTO:
    id: WishListId


class WishDbGateway(
    WishListReader,
    ShareReader, Protocol,
):
    pass


class ViewWishList(Interactor[ViewWishListDTO, WishList]):
    def __init__(
            self,
            wish_db_gateway: WishDbGateway,
            access_service: AccessService,
            id_provider: IdProvider,
    ):
        self.wish_db_gateway = wish_db_gateway
        self.access_service = access_service
        self.id_provider = id_provider

    def __call__(self, data: ViewWishListDTO) -> WishList:
        user_id = self.id_provider.get_current_user_id()
        wishlist: WishList = self.wish_db_gateway.get_wishlist(data.id)
        share_rules = self.wish_db_gateway.get_share_rules(wishlist.id, user_id)

        self.access_service.ensure_can_view(wishlist, user_id, share_rules)
        return wishlist
