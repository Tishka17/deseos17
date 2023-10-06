from abc import abstractmethod, ABC
from typing import ContextManager

from deseos17.application.create_wish.interactor import CreateWish
from deseos17.application.view_wishlist.Interactor import ViewWishList


class InteractorFactory(ABC):
    @abstractmethod
    def create_wish(self) -> ContextManager[CreateWish]:
        raise NotImplementedError

    @abstractmethod
    def view_wishlist(self) -> ContextManager[ViewWishList]:
        raise NotImplementedError
