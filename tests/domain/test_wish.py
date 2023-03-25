import datetime

from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import Wish, WishId, WishListId, WishList
from deseos17.domain.services.wish import WishService


def test_wish_update():
    old_time = datetime.datetime(1, 1, 1, 0, 0)
    wish = Wish(
        id=WishId(0),
        text="old",
        updated_at=old_time,
        wishlist_id=WishListId(0)
    )
    wishlist = WishList(
        updated_at=old_time,
        title="old_name",
        id=WishListId(0),
        owner_id=UserId(0),
    )

    WishService().update_wish(wish, wishlist, "new_text")
    assert wish.text == "new_text"
    assert wish.updated_at > old_time
    assert wish.updated_at == wishlist.updated_at
