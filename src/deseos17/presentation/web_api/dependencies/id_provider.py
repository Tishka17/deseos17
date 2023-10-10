from fastapi import Cookie
from typing_extensions import Annotated

from deseos17.adapters.auth.token import (
    JwtTokenProcessor, TokenIdProvider,
)
from deseos17.application.common.id_provider import IdProvider


def get_id_provider(
        token_processor: JwtTokenProcessor,
        token: Annotated[str, Cookie()],
) -> IdProvider:
    return TokenIdProvider(
        token_processor=token_processor,
        token=token,
    )
