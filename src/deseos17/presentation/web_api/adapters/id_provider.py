from typing import Annotated

from fastapi import Cookie

from deseos17.application.common.id_provider import IdProvider
from deseos17.domain.models.user_id import UserId
from deseos17.presentation.web_api.token import TokenProcessor


class HttpIdProvider(IdProvider):
    def __init__(
            self,
            http_authenticator: TokenProcessor,
            token: Annotated[str, Cookie()],
    ):
        self.http_authenticator = http_authenticator
        self.token = token

    def get_current_user_id(self) -> UserId:
        return self.http_authenticator.validate_token(self.token)
