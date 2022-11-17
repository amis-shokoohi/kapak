import os
from pathlib import Path
from typing import Optional

from kapak.constant import BUFFER_SIZE
from kapak.logger import LoggerType, LoggerDefault
from kapak.key import derive_key
from kapak.progress import ProgressType, ProgressDefault
from kapak.error import KapakError
import kapak.aes


class Encryptor:
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

    def encrypt(self, src: Path, password: str, remove_: bool = False) -> Path:
        if not src.exists():
            raise KapakError(f"can not find {src}")

        if src.is_file():
            return self._encrypt_file(src, password, remove_)

        raise KapakError(f"{src} is not a file")

    def _encrypt_file(self, src: Path, password: str, remove_: bool) -> Path:
        src_size = src.stat().st_size
        if src_size == 0:
            raise KapakError(f"{src} is empty")

        dest = src.with_suffix(".kpk")
        if dest.exists():  # Overwrite error
            raise KapakError(f"{dest} already exists")

        salt = os.urandom(16)
        key = derive_key(password, salt)

        self._logger.info("Encrypting...")
        self._progress.set_total(src_size)
        for p in kapak.aes.encrypt(src, dest, key, salt, self._buffer_size):
            self._progress.update(p)
        if remove_:
            src.unlink()

        return dest
