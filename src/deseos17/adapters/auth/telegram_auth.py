from typing import Mapping

from aiogram.utils.auth_widget import check_signature

from deseos17.application.common.id_provider import IdProvider
from deseos17.domain.models.user_id import UserId


class TelegramAuthenticator:
    def __init__(self, token: str):
        self.token = token

    def validate(self, hash: str, fields: Mapping[str, str]) -> bool:
        fields = {
            k: v
            for k, v in fields.items()
            if v is not None and k != "hash"
        }
        return check_signature(
            token=self.token,
            hash=hash,
            **fields,
        )


class TelegramAuthIdProvider(IdProvider):
    def __init__(
            self,
            authenticator: TelegramAuthenticator,
            hash: str,
            fields: Mapping[str, str],
    ):
        self.authenticator = authenticator
        self.hash = hash
        self.fields = fields

    def get_current_user_id(self) -> UserId:
        self.authenticator.validate(self.hash, self.fields)
        return UserId(int(self.fields["id"]))
