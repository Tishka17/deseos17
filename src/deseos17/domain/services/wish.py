from datetime import datetime

from ..models.user_id import UserId
from ..models.wish import Wish, WishList


def update_wish(wish: Wish, wishlist: WishList, new_text: str) -> None:
    wish.text = new_text
    wish.updated_at = datetime.now()
    wishlist.updated_at = wish.updated_at


def create_wish(
        wishlist: WishList, text: str, owner_id: UserId,
) -> Wish:
    wishlist.updated_at = datetime.now()
    return Wish(
        owner_id=owner_id,
        wishlist_id=wishlist.id,
        id=None,
        text=text,
        updated_at=wishlist.updated_at,
    )
