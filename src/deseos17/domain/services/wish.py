from datetime import datetime

from ..models.wish import Wish, WishList


def update_wish(wish: Wish, wishlist: WishList, new_text: str) -> None:
    wish.text = new_text
    wish.updated_at = datetime.now()
    wishlist.updated_at = wish.updated_at
