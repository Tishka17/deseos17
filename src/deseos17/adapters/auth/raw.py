from deseos17.application.common.id_provider import IdProvider
from deseos17.domain.models.user_id import UserId


class RawIdProvider(IdProvider):
    def __init__(
            self,
            user_id: UserId,
    ):
        self.user_id = user_id

    def get_current_user_id(self) -> UserId:
        return self.user_id
