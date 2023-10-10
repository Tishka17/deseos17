from dataclasses import dataclass

from .user_id import UserId


@dataclass
class User:
    id: UserId
    username: str
