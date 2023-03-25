from datetime import datetime

from ..models.user_id import UserId
from ..models.wish import WishList


class WishListService:
    def create_wishlist(
            self, title: str, user_id: UserId,
    ) -> WishList:
        return WishList(
            id=None,
            title=title,
            updated_at=datetime.now(),
            owner_id=user_id,
        )
