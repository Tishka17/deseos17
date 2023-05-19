from typing import Protocol

from deseos17.application.common.interfaces import (
    WishListReader, ShareReader,
)


class DbGateway(
    WishListReader,
    ShareReader, Protocol,
):
    pass
