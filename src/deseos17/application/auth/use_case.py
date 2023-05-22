from deseos17.application.common.use_case import UseCase

from .dto import LoginResultDTO
from .interfaces import Authenticator
from ...domain.models.user_id import UserId


class CreateWish(UseCase[LoginResultDTO, UserId]):
    def __init__(
            self,
            authenticator: Authenticator,
    ):
        self.authenticator = authenticator

    def __call__(self, data: LoginResultDTO) -> UserId:
        self.authenticator.validate(data)
        return UserId(data.id)
