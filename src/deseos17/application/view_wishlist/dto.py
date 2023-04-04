from dataclasses import dataclass

from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId


@dataclass
class ViewWishListDTO:
    user_id: UserId
    id: WishListId
