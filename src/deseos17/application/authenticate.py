from dataclasses import dataclass
from typing import Optional

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.interactor import Interactor
from deseos17.application.common.transaction import TransactionManager
from deseos17.application.common.user_gateway import UserSaver
from deseos17.domain.models.user import User
from deseos17.domain.models.user_id import UserId


@dataclass
class LoginResultDTO:
    id: int
    auth_date: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None


class Authenticate(Interactor[LoginResultDTO, UserId]):
    def __init__(
            self,
            id_provider: IdProvider,
            user_saver: UserSaver,
            transaction_manager: TransactionManager,
    ):
        self.id_provider = id_provider
        self.user_saver = user_saver
        self.transaction_manager = transaction_manager

    def __call__(self, data: LoginResultDTO) -> UserId:
        user_id = self.id_provider.get_current_user_id()
        self.user_saver.save_user(User(
            id=user_id,
            username=data.username,
        ))
        self.transaction_manager.commit()
        return user_id
