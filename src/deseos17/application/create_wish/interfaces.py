from typing import Protocol

from deseos17.application.common.interfaces import (
    Comitter, WishReader, WishListReader, WishSaver, WishListSaver,
    ShareReader,
)


class DbGateway(
    Protocol, Comitter, WishReader, WishListReader, WishSaver, WishListSaver,
    ShareReader,
):
    pass
