from dataclasses import dataclass

from .user_id import UserID


@dataclass
class User:
    user_id: UserID
