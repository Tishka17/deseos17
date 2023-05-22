import hmac
from hashlib import sha256

from deseos17.application.auth.dto import LoginResultDTO
from deseos17.application.auth.interfaces import Authenticator


class TelegramAuthenticator(Authenticator):
    def __init__(self, token: str):
        self.secret_key = sha256(token.encode("utf-8")).digest()

    def validate(self, data: LoginResultDTO) -> bool:
        data_list = [
            f"auth_date={data.auth_date}",
            f"first_name={data.first_name}",
            f"hash={data.hash}",
            f"id={data.id}",
            f"photo_url={data.photo_url}",
            f"username={data.username}",
        ]
        data_list.sort()
        expected_hash = hmac.new(
            key=self.secret_key,
            msg="\n".join(data_list).encode("utf-8"),
            digestmod=sha256
        ).hexdigest()
        return expected_hash == data.hash
