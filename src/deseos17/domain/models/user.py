from dataclasses import dataclass

from .user_id import UserId


@dataclass
class User:
    user_id: UserId
