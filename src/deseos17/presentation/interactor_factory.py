from abc import abstractmethod, ABC
from typing import ContextManager

from deseos17.application.create_wish import CreateWish
from deseos17.application.view_wishlist import ViewWishList


class InteractorFactory(ABC):
    @abstractmethod
    def create_wish(self) -> ContextManager[CreateWish]:
        raise NotImplementedError

    @abstractmethod
    def view_wishlist(self) -> ContextManager[ViewWishList]:
        raise NotImplementedError
