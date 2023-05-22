from deseos17.application.common.use_case import UseCase

from .dto import LoginResultDTO
from .interfaces import Authenticator
from ...domain.exceptions.access import AuthenticationError
from ...domain.models.user_id import UserId


class Authenticate(UseCase[LoginResultDTO, UserId]):
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
