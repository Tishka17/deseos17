from dataclasses import dataclass


@dataclass
class LoginResultDTO:
    id: int
    first_name: str
    username: str
    photo_url: str
    auth_date: int
    hash: str
