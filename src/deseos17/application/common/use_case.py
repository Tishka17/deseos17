from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class UseCase(Generic[InputDTO, OutputDTO]):
    def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError
