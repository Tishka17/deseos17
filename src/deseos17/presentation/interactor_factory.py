from abc import abstractmethod
from typing import Protocol, ContextManager

from deseos17.application.create_wish.use_case import CreateWish
from deseos17.application.view_wishlist.use_case import ViewWishList


class InteractorFactory(Protocol):
    @abstractmethod
    def create_wish(self) -> ContextManager[CreateWish]:
        raise NotImplementedError

    @abstractmethod
    def view_wishlist(self) -> ContextManager[ViewWishList]:
        raise NotImplementedError
