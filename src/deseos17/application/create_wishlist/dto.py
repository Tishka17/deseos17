from dataclasses import dataclass

from deseos17.domain.models.user_id import UserId


@dataclass
class NewWishListDTO:
    user_id: UserId
    title: str
