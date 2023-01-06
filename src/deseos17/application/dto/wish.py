from dataclasses import dataclass

from ...domain.models.wish import WishId


@dataclass
class UpdateWishDTO:
    id: WishId
    text: str
