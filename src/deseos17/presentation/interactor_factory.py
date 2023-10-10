from abc import abstractmethod, ABC
from typing import ContextManager

from deseos17.application.authenticate import Authenticate
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wish import CreateWish
from deseos17.application.create_wishlist import CreateWishList
from deseos17.application.get_own_wishlists import GetOwnWishLists
from deseos17.application.update_wish import UpdateWish
from deseos17.application.view_wishlist import ViewWishList


class InteractorFactory(ABC):
    @abstractmethod
    def authenticate(
            self, id_provider: IdProvider,
    ) -> ContextManager[Authenticate]:
        raise NotImplementedError

    @abstractmethod
    def create_wish(
            self, id_provider: IdProvider,
    ) -> ContextManager[CreateWish]:
        raise NotImplementedError

    @abstractmethod
    def create_wishlist(
            self, id_provider: IdProvider,
    ) -> ContextManager[CreateWishList]:
        raise NotImplementedError

    @abstractmethod
    def get_own_wishlists(
            self, id_provider: IdProvider,
    ) -> ContextManager[GetOwnWishLists]:
        raise NotImplementedError

    @abstractmethod
    def update_wish(
            self, id_provider: IdProvider,
    ) -> ContextManager[UpdateWish]:
        raise NotImplementedError

    @abstractmethod
    def view_wishlist(
            self, id_provider: IdProvider,
    ) -> ContextManager[ViewWishList]:
        raise NotImplementedError
