import hmac
from hashlib import sha256

from deseos17.application.authenticate import Authenticator, LoginResultDTO
from aiogram.utils.auth_widget import check_signature


class TelegramAuthenticator(Authenticator):
    def __init__(self, token: str):
        self.token = token

    def validate(self, data: LoginResultDTO) -> bool:
        fields = {
            "id": data.id,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "username": data.username,
            "photo_url": data.photo_url,
            "auth_date": data.auth_date,
        }
        fields = {
            k: v
            for k, v in fields.items()
            if v is not None
        }
        return check_signature(
            token=self.token,
            hash=data.hash,
            **fields,
        )
