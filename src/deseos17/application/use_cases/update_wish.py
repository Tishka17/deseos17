from deseos17.domain.models.user_id import UserID
from deseos17.domain.models.wish import Wish, WishList
from deseos17.domain.services.access import user_can_edit
from deseos17.domain.services.wish import update_wish
from ..dto.wish import UpdateWishDTO
from ..exceptions import AccessDenied


class UpdateWish:
    def __init__(self, db_gateway):
        self.db_gateway = db_gateway

    def __call__(self, data: UpdateWishDTO, user_id: UserID) -> None:
        wish: Wish = self.db_gateway.get_wish(data.id)
        wishlist: WishList = self.db_gateway.get_wishlist(wish.wishlist_id)
        share_rules = self.db_gateway.get_share_rules(wishlist.id, user_id)

        if not user_can_edit(wish, user_id, share_rules):
            raise AccessDenied

        update_wish(wish, wishlist, new_text=data.text)
        self.db_gateway.save_wish(wish)
        self.db_gateway.save_wishlist(wishlist)
        self.db_gateway.commit()
