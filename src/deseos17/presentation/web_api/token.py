from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from starlette import status

from deseos17.domain.exceptions.access import AuthenticationError
from deseos17.domain.models.user_id import UserId


class TokenProcessor(ABC):

    @abstractmethod
    def create_access_token(self, user_id: UserId) -> str:
        raise NotImplementedError

    @abstractmethod
    def validate_token(self, token: str) -> UserId:
        raise NotImplementedError
