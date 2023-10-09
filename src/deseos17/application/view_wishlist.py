from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.interfaces import (
    WishListReader, ShareReader,
)
from deseos17.domain.models.wish import WishList
from deseos17.domain.models.wish import WishListId
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService


@dataclass
class ViewWishListDTO:
    id: WishListId


class DbGateway(
    WishListReader,
    ShareReader, Protocol,
):
    pass


class ViewWishList(Interactor[ViewWishListDTO, WishList]):
    def __init__(
            self,
            db_gateway: DbGateway,
            access_service: AccessService,
            wish_service: WishService,
            id_provider: IdProvider,
    ):
        self.db_gateway = db_gateway
        self.access_service = access_service
        self.wish_service = wish_service
        self.id_provider = id_provider

    def __call__(self, data: ViewWishListDTO) -> WishList:
        user_id = self.id_provider.get_current_user_id()
        wishlist: WishList = self.db_gateway.get_wishlist(data.id)
        share_rules = self.db_gateway.get_share_rules(wishlist.id, user_id)

        self.access_service.ensure_can_view(wishlist, user_id, share_rules)
        return wishlist
