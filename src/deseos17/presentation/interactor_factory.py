from abc import abstractmethod, ABC
from typing import ContextManager

from deseos17.application.auth.use_case import Authenticate
from deseos17.application.create_wish.use_case import CreateWish
from deseos17.application.view_wishlist.use_case import ViewWishList


class InteractorFactory(ABC):
    @abstractmethod
    def authenticate(self) -> ContextManager[Authenticate]:
        raise NotImplementedError

    @abstractmethod
    def create_wish(self) -> ContextManager[CreateWish]:
        raise NotImplementedError

    @abstractmethod
    def view_wishlist(self) -> ContextManager[ViewWishList]:
        raise NotImplementedError
