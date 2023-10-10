from dataclasses import dataclass
from typing import List

from deseos17.application.common.dto import Pagination
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.wish_gateway import (
    WishListsReader,
)
from deseos17.domain.models.wish import WishList


@dataclass
class GetOwnWishListsDTO:
    pagination: Pagination


@dataclass
class OwnWishListsResultDTO:
    total: int
    wishlists: List[WishList]


class GetOwnWishLists(Interactor[GetOwnWishListsDTO, WishList]):
    def __init__(
            self,
            wish_db_gateway: WishListsReader,
            id_provider: IdProvider,
    ):
        self.wish_db_gateway = wish_db_gateway
        self.id_provider = id_provider

    def __call__(self, data: GetOwnWishListsDTO) -> OwnWishListsResultDTO:
        user_id = self.id_provider.get_current_user_id()
        total = self.wish_db_gateway.total_wishlists(user_id)
        wishlists = self.wish_db_gateway.find_wishlists(
            owner_id=user_id,
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )
        return OwnWishListsResultDTO(
            total=total,
            wishlists=wishlists,
        )
