from dataclasses import dataclass

from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishId


@dataclass
class UpdateWishDTO:
    user_id: UserId
    id: WishId
    text: str
