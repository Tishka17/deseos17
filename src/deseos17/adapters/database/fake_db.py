from datetime import datetime
from typing import List

from deseos17.application.create_wish.interfaces import (
    DbGateway as CreateWishDbGateway,
)
from deseos17.application.view_wishlist.interfaces import (
    DbGateway as ViewWishListDbGateway,
)
from deseos17.domain.models.sharing import ShareRule
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId, WishList, Wish


class FakeGateway(ViewWishListDbGateway, CreateWishDbGateway):
    def commit(self):
        pass

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
