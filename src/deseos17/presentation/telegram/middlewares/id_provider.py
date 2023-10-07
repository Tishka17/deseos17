from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject

from deseos17.application.common.id_provider import IdProvider
from deseos17.domain.models.user_id import UserId


class TelegramIdProvider(IdProvider):
    def __init__(self, user: User):
        self.user = user

    def get_current_user_id(self) -> UserId:
        return UserId(self.user.id)


class IdProviderMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        if user := data.get("event_from_user"):
            data["id_provider"] = TelegramIdProvider(user)
        return await handler(event, data)
