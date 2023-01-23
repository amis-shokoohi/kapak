import sys
from pathlib import Path
from typing import Optional, TypeVar, Any


Self = TypeVar("Self", bound="Pipe")


class Pipe:
    def __init__(self, src: Optional[Path], dst: Optional[Path]) -> None:
        self.src_is_file = src is not None
        self.dst_is_file = dst is not None

        if src is None:
            self.src = sys.stdin.buffer
        else:
            self.src = src.open(mode="rb")

        if dst is None:
            self.dst = sys.stdout.buffer
        else:
            self.dst = dst.open(mode="wb")

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        if self.src_is_file:
            self.src.close()

        if self.dst_is_file:
            self.dst.close()
        else:
            self.dst.flush()
