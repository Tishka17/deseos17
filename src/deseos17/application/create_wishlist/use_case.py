from deseos17.application.common.use_case import UseCase
from deseos17.domain.models.wish import WishListId
from deseos17.domain.services.wishlist import create_wishlist

from .dto import NewWishListDTO
from .interfaces import DbGateway


class CreateWishList(UseCase[NewWishListDTO, WishListId]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    def __call__(self, data: NewWishListDTO) -> WishListId:
        wishlist = create_wishlist(user_id=data.user_id, title=data.title)

        self.db_gateway.save_wishlist(wishlist)
        self.db_gateway.commit()
        return wishlist.id
