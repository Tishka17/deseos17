from deseos17.application.common.transaction import TransactionManager


class FakeTransactionManager(TransactionManager):
    def flush(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def commit(self) -> None:
        pass
