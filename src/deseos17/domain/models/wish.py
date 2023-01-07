from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from .user import UserId

WishId = NewType("WishId", int)
WishListId = NewType("WishListId", int)


@dataclass
class WishList:
    id: WishListId
    name: str
    updated_at: datetime


@dataclass
class Wish:
    id: WishId
    text: str
    updated_at: datetime
    wishlist_id: WishListId
    owner_id: UserId
