from dataclasses import dataclass

from .user_id import UserId
from .wish import WishListId


@dataclass
class ShareRule:
    wishlist_id: WishListId
    user_id: UserId
    read_allowed: bool
    write_allowed: bool
