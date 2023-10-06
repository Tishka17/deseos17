from deseos17.application.common.interactor import Interactor
from deseos17.domain.models.wish import WishListId
from deseos17.domain.services.wishlist import WishListService

from .dto import NewWishListDTO
from .interfaces import DbGateway


class CreateWishList(Interactor[NewWishListDTO, WishListId]):
    def __init__(
            self,
            db_gateway: DbGateway,
            wishlist_service: WishListService,
    ):
        self.db_gateway = db_gateway
        self.wishlist_service = wishlist_service

    def __call__(self, data: NewWishListDTO) -> WishListId:
        wishlist = self.wishlist_service.create_wishlist(
            user_id=data.user_id, title=data.title,
        )

        self.db_gateway.save_wishlist(wishlist)
        self.db_gateway.commit()
        return wishlist.id
