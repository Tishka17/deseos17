from typing import Callable, Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class UseCase(Generic[InputDTO, OutputDTO]):
    def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


UseCaseT = TypeVar("UseCaseT")
UseCaseFactory = Callable[[], UseCaseT]
