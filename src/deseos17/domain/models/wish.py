from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Optional

from .user import UserId

WishId = NewType("WishId", int)
WishListId = NewType("WishListId", int)


@dataclass
class WishList:
    id: Optional[WishListId]
    owner_id: UserId
    title: str
    updated_at: datetime


@dataclass
class Wish:
    id: Optional[WishId]
    text: str
    updated_at: datetime
    wishlist_id: WishListId
