from datetime import datetime
from typing import List

from deseos17.application.common.wish_gateway import (
    WishReader, WishSaver,
    WishListReader, WishListsReader, WishListSaver,
    ShareReader,
)
from deseos17.domain.models.sharing import ShareRule
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId, WishList, Wish, WishId


class FakeWishGateway(
    WishReader, WishSaver,
    WishListReader, WishListsReader, WishListSaver,
    ShareReader,
):
    def get_wish(self, wish_id: WishId) -> Wish:
        return Wish(
            id=wish_id,
            updated_at=datetime.min,
            wishlist_id=WishListId(0),
            text=f"Wish {wish_id}",
        )

    def find_wishlists(
            self,
            owner_id: UserId,
            limit: int,
            offset: int,
    ) -> List[WishList]:
        if limit == 0:
            return []
        return [
            WishList(
                id=WishListId(i),
                updated_at=datetime.min,
                owner_id=owner_id,
                title=f"Wishlist {i}"
            )
            for i in range(offset, offset + limit)
        ]

    def total_wishlists(self, owner_id: UserId) -> int:
        return 20

    def get_wishlist(self, wishlist_id: WishListId) -> WishList:
        return WishList(
            id=wishlist_id,
            owner_id=UserId(0),
            title="Fake title",
            updated_at=datetime.now(),
        )

    def save_wish(self, wish: Wish) -> None:
        pass

    def save_wishlist(self, wish: WishList) -> None:
        pass

    def get_share_rules(
            self, wishlist_id: WishListId, user_id: UserId,
    ) -> List[ShareRule]:
        return []
