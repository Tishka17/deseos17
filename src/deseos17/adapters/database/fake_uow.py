from deseos17.application.common.uow import UoW


class FakeUoW(UoW):
    def flush(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def commit(self) -> None:
        pass
