from dataclasses import dataclass

from .user_id import UserID
from .wish import WishListId


@dataclass
class ShareRule:
    wishlist_id: WishListId
    user_id: UserID
    read_allowed: bool
    write_allowed: bool
