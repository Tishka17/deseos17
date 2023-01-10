from dataclasses import dataclass

from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId


@dataclass
class NewWishDTO:
    wishlist_id: WishListId
    user_id: UserId
    text: str
