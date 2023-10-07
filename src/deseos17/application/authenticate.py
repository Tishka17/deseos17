from dataclasses import dataclass
from typing import Protocol

from deseos17.application.common.interactor import Interactor
from deseos17.domain.exceptions.access import AuthenticationError
from deseos17.domain.models.user_id import UserId


@dataclass
class LoginResultDTO:
    id: int
    first_name: str
    username: str
    photo_url: str
    auth_date: int
    hash: str


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
