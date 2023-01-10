from typing import Protocol, List

from deseos17.domain.models.sharing import ShareRule
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishListId, WishId, Wish, WishList


class Comitter(Protocol):
    def commit(self):
        raise NotImplementedError


class WishReader(Protocol):
    def get_wish(self, wish_id: WishId) -> Wish:
        raise NotImplementedError


class WishSaver(Protocol):
    def save_wish(self, wish: Wish) -> None:
        raise NotImplementedError


class WishListReader(Protocol):

    def get_wishlist(self, wishlist_id: WishListId) -> WishList:
        raise NotImplementedError


class WishListSaver(Protocol):
    def save_wishlist(self, wish: WishList) -> None:
        raise NotImplementedError


class ShareReader(Protocol):
    def get_share_rules(
            self, wishlist_id: WishListId, user_id: UserId,
    ) -> List[ShareRule]:
        raise NotImplementedError
