from dataclasses import dataclass
from typing import Protocol, Optional

from deseos17.application.common.interactor import Interactor
from deseos17.domain.exceptions.access import AuthenticationError
from deseos17.domain.models.user_id import UserId


@dataclass
class LoginResultDTO:
    id: int
    auth_date: int
    hash: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None


class Authenticator(Protocol):
    def validate(self, data: LoginResultDTO) -> bool:
        raise NotImplementedError


class Authenticate(Interactor[LoginResultDTO, UserId]):
    def __init__(
            self,
            authenticator: Authenticator,
    ):
        self.authenticator = authenticator

    def __call__(self, data: LoginResultDTO) -> UserId:
        if not self.authenticator.validate(data):
            raise AuthenticationError
        # TODO: save user to DB
        return UserId(data.id)
