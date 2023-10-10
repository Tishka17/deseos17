from abc import abstractmethod
from typing import Protocol

from deseos17.domain.models.user import User
from deseos17.domain.models.user_id import UserId


class UserReader(Protocol):
    @abstractmethod
    def get_user(self, user_id: UserId) -> User:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    def save_user(self, user: User) -> None:
        raise NotImplementedError
