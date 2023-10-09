from abc import abstractmethod, ABC
from typing import ContextManager

from deseos17.application.authenticate import Authenticate
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wish import CreateWish
from deseos17.application.view_wishlist import ViewWishList


class InteractorFactory(ABC):
    @abstractmethod
    def authenticate(self) -> ContextManager[Authenticate]:
        raise NotImplementedError

    @abstractmethod
    def create_wish(
            self, id_provider: IdProvider,
    ) -> ContextManager[CreateWish]:
        raise NotImplementedError

    @abstractmethod
    def view_wishlist(
            self, id_provider: IdProvider,
    ) -> ContextManager[ViewWishList]:
        raise NotImplementedError
