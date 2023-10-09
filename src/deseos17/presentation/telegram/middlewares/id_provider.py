from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from deseos17.adapters.auth.raw import RawIdProvider
from deseos17.domain.models.user_id import UserId


class IdProviderMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        if user := data.get("event_from_user"):
            data["id_provider"] = RawIdProvider(UserId(user.id))
        return await handler(event, data)
