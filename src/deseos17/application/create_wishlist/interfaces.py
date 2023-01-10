from typing import Protocol

from deseos17.application.common.interfaces import (
    Comitter, WishListSaver,
)


class DbGateway(
    Protocol, Comitter, WishListSaver,
):
    pass
