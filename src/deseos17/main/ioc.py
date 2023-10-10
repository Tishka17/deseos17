from contextlib import contextmanager
from typing import ContextManager

from deseos17.adapters.database.fake_uow import FakeUoW
from deseos17.adapters.database.fake_user_db import FakeUserGateway
from deseos17.adapters.database.fake_wish_db import FakeWishGateway
from deseos17.application.authenticate import Authenticate
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wish import CreateWish
from deseos17.application.create_wishlist import CreateWishList
from deseos17.application.get_own_wishlists import GetOwnWishLists
from deseos17.application.update_wish import UpdateWish
from deseos17.application.view_wishlist import ViewWishList
from deseos17.domain.services.access import AccessService
from deseos17.domain.services.wish import WishService
from deseos17.domain.services.wishlist import WishListService
from deseos17.presentation.interactor_factory import InteractorFactory


class IoC(InteractorFactory):
    def __init__(self, tg_token: str):
        self.wish_gateway = FakeWishGateway()
        self.user_gateway = FakeUserGateway()
        self.uow = FakeUoW()
        self.tg_token = tg_token

    @contextmanager
    def authenticate(
            self, id_provider: IdProvider,
    ) -> Authenticate:
        yield Authenticate(
            id_provider=id_provider,
            user_saver=self.user_gateway,
            uow=self.uow,
        )

    @contextmanager
    def create_wish(
            self, id_provider: IdProvider,
    ) -> CreateWish:
        yield CreateWish(
            wish_db_gateway=self.wish_gateway,
            uow=self.uow,
            access_service=AccessService(),
            wish_service=WishService(),
            id_provider=id_provider,
        )

    @contextmanager
    def create_wishlist(
            self, id_provider: IdProvider,
    ) -> ContextManager[CreateWishList]:
        yield CreateWishList(
            wish_db_gateway=self.wish_gateway,
            uow=self.uow,
            id_provider=id_provider,
            wishlist_service=WishListService(),
        )

    @contextmanager
    def get_own_wishlists(
            self, id_provider: IdProvider,
    ) -> ContextManager[GetOwnWishLists]:
        yield GetOwnWishLists(
            id_provider=id_provider,
            wish_db_gateway=self.wish_gateway,
        )

    @contextmanager
    def update_wish(
            self, id_provider: IdProvider,
    ) -> ContextManager[UpdateWish]:
        yield UpdateWish(
            wish_db_gateway=self.wish_gateway,
            uow=self.uow,
            id_provider=id_provider,
            access_service=AccessService(),
            wish_service=WishService(),
        )

    @contextmanager
    def view_wishlist(
            self, id_provider: IdProvider,
    ) -> ViewWishList:
        yield ViewWishList(
            wish_db_gateway=self.wish_gateway,
            access_service=AccessService(),
            id_provider=id_provider,
        )
