from deseos17.application.common.interactor import Interactor
from deseos17.domain.models.wish import WishList
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService
from .dto import ViewWishListDTO
from .interfaces import DbGateway


class ViewWishList(Interactor[ViewWishListDTO, WishList]):
    def __init__(
            self,
            db_gateway: DbGateway,
            access_service: AccessService,
            wish_service: WishService,
    ):
        self.db_gateway = db_gateway
        self.access_service = access_service
        self.wish_service = wish_service

    def __call__(self, data: ViewWishListDTO) -> WishList:
        wishlist: WishList = self.db_gateway.get_wishlist(data.id)
        share_rules = self.db_gateway.get_share_rules(
            wishlist.id, data.user_id,
        )

        self.access_service.ensure_can_view(
            wishlist, data.user_id, share_rules,
        )
        return wishlist
