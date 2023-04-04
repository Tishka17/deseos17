from typing import List

from ..exceptions.access import AccessDenied
from ..models.sharing import ShareRule
from ..models.user_id import UserId
from ..models.wish import WishList


class AccessService:
    def ensure_can_edit(
            self, wishlist: WishList, user_id: UserId,
            share_rules: List[ShareRule],
    ) -> None:
        if wishlist.owner_id == user_id:
            return
        for share_rule in share_rules:
            if share_rule.user_id == user_id and share_rule.write_allowed:
                return
        raise AccessDenied()

    def ensure_can_create(
            self, wishlist: WishList, user_id: UserId,
            share_rules: List[ShareRule],
    ) -> None:
        if wishlist.owner_id == user_id:
            return
        for share_rule in share_rules:
            if share_rule.user_id == user_id and share_rule.write_allowed:
                return
        raise AccessDenied()
