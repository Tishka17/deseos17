from typing import Protocol

from deseos17.application.common.interfaces import (
    Comitter, WishListReader, WishSaver, WishListSaver,
    ShareReader,
)


class DbGateway(
    Comitter, WishListReader, WishSaver, WishListSaver,
    ShareReader, Protocol,
):
    pass
