from deseos17.application.common.user_gateway import UserSaver, UserReader
from deseos17.domain.models.user import User
from deseos17.domain.models.user_id import UserId


class FakeUserGateway(UserReader, UserSaver):
    def get_user(self, user_id: UserId) -> User:
        return User(
            id=user_id,
            username=f"Name {user_id}"
        )

    def save_user(self, user: User) -> None:
        pass
