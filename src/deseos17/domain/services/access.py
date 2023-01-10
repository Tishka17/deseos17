from typing import List

from ..models.sharing import ShareRule
from ..models.user_id import UserId
from ..models.wish import WishList


def user_can_edit(
        wishlist: WishList, user_id: UserId, share_rules: List[ShareRule],
) -> bool:
    if wishlist.owner_id == user_id:
        return True
    for share_rule in share_rules:
        if share_rule.user_id == user_id and share_rule.write_allowed:
            return True
    return False


def user_can_create(
        wishlist: WishList, user_id: UserId, share_rules: List[ShareRule],
) -> bool:
    if wishlist.owner_id == user_id:
        return True
    for share_rule in share_rules:
        if share_rule.user_id == user_id and share_rule.write_allowed:
            return True
    return False
