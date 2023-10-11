from dataclasses import dataclass
from typing import Protocol, List

from deseos17.application.common.dto import Pagination
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.wish_gateway import (
    WishListReader, ShareReader, WishesReader,
)
from deseos17.domain.models.wish import WishList, WishListId, Wish
from deseos17.domain.services.access import AccessService


@dataclass
class ViewWishListDTO:
    id: WishListId
    pagination: Pagination


@dataclass
class WishListResultDTO:
    wishlist: WishList
    total_wishes: int
    wishes: List[Wish]


class WishDbGateway(
    WishListReader, WishesReader,
    ShareReader, Protocol,
):
    pass


class ViewWishList(Interactor[ViewWishListDTO, WishListResultDTO]):
    def __init__(
            self,
            wish_db_gateway: WishDbGateway,
            access_service: AccessService,
            id_provider: IdProvider,
    ):
        self.wish_db_gateway = wish_db_gateway
        self.access_service = access_service
        self.id_provider = id_provider

    def __call__(self, data: ViewWishListDTO) -> WishListResultDTO:
        user_id = self.id_provider.get_current_user_id()
        wishlist = self.wish_db_gateway.get_wishlist(data.id)
        share_rules = self.wish_db_gateway.get_share_rules(
            wishlist.id, user_id,
        )

        self.access_service.ensure_can_view(wishlist, user_id, share_rules)

        total = self.wish_db_gateway.total_wishlists_for_list(wishlist.id)
        wishes = self.wish_db_gateway.find_wishes_for_list(
            wishlist_id=wishlist.id,
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )

        return WishListResultDTO(
            total_wishes=total,
            wishes=wishes,
            wishlist=wishlist,
        )
