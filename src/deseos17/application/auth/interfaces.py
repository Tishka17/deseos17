from typing import Protocol

from .dto import LoginResultDTO


class Authenticator(Protocol):
    def validate(self, data: LoginResultDTO) -> bool:
        raise NotImplementedError
