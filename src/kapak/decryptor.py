from pathlib import Path
from typing import List, Optional

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

    def decrypt(self, src: Path, password: str, remove_: bool = False) -> None:
        if not src.exists():
            raise KapakError(f"can not find {src}")

        if src.is_file():
            return self._decrypt_file(src, password, remove_)
        elif src.is_dir():
            return self._decrypt_dir(src, password, remove_)
        else:
            raise KapakError(f"{src} is neither a file nor a directory")

    def _decrypt_file(self, src: Path, password: str, remove_: bool) -> None:
        if not src.match("*.kpk"):
            raise KapakError(f"can not decrypt {src}")

        src_size = src.stat().st_size
        if src_size == 0:
            raise KapakError(f"{src} is empty")

        self._logger.info("Decrypting...")
        self._progress.set_total(src_size)
        for p in kapak.aes.decrypt(src, password, self._buffer_size):
            self._progress.update(p)

        if remove_:
            src.unlink()

    def _decrypt_dir(self, src: Path, password: str, remove_: bool) -> None:
        self._logger.info("Scanning the directory...")
        ff: List[Path] = []
        src_size = 0
        for f in src.rglob("*.kpk"):
            ff.append(f)
            src_size += f.stat().st_size
        if len(ff) == 0 or src_size == 0:
            raise KapakError(f"{src} is empty")

        self._logger.info("Decrypting...")
        self._progress.set_total(src_size)
        for f in ff:
            for p in kapak.aes.decrypt(f, password, self._buffer_size):
                self._progress.update(p)
            if remove_:
                f.unlink()
