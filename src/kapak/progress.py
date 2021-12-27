from typing import Protocol, runtime_checkable


@runtime_checkable
class ProgressType(Protocol):
    def set_total(self, total: int) -> None:
        pass

    def update(self, part: int) -> None:
        pass


class ProgressDefault:
    def set_total(self, total: int) -> None:
        pass

    def update(self, part: int) -> None:
        pass
