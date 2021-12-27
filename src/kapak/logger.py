from typing import Protocol, runtime_checkable


@runtime_checkable
class LoggerType(Protocol):
    def info(self, msg: str, end: str = "\n") -> None:
        pass


class LoggerDefault:
    def info(self, msg: str, end: str = "\n") -> None:
        pass
