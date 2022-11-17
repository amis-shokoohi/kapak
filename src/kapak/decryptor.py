from pathlib import Path
from typing import Optional

from kapak.constant import BUFFER_SIZE
from kapak.logger import LoggerType, LoggerDefault
from kapak.progress import ProgressType, ProgressDefault
from kapak.error import KapakError
import kapak.aes


class Decryptor:
    def __init__(
        self,
        buffer_size: int = BUFFER_SIZE,
        logger: Optional[LoggerType] = None,
        progress: Optional[ProgressType] = None,
    ) -> None:
        self._buffer_size = buffer_size * 1024 * 1024

        if logger is not None:
            assert isinstance(logger, LoggerType)
            self._logger = logger
        else:
            self._logger = LoggerDefault()

        if progress is not None:
            assert isinstance(progress, ProgressType)
            self._progress = progress
        else:
            self._progress = ProgressDefault()

    def decrypt(self, src: Path, password: str) -> None:
        if not src.exists():
            raise KapakError(f"can not find {src}")

        if src.is_file():
            return self._decrypt_file(src, password)

        raise KapakError(f"{src} is not a file")

    def _decrypt_file(self, src: Path, password: str) -> None:
        if not src.match("*.kpk"):
            raise KapakError(f"can not decrypt {src}")

        src_size = src.stat().st_size
        if src_size == 0:
            raise KapakError(f"{src} is empty")

        self._logger.info("Decrypting...")
        self._progress.set_total(src_size)
        for p in kapak.aes.decrypt(src, password, self._buffer_size):
            self._progress.update(p)
