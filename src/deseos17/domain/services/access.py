from typing import List

from ..models.sharing import ShareRule
from ..models.user_id import UserID
from ..models.wish import Wish


def user_can_edit(
        wish: Wish, user_id: UserID, share_rules: List[ShareRule],
) -> bool:
    if wish.owner_id == user_id:
        return True
    for share_rule in share_rules:
        if share_rule.user_id == user_id and share_rule.write_allowed:
            return True
    return False
