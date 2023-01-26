import sys


class Progress:
    _space = 20 * " "
    _bar = [
        "□□□□□□□□□□",
        "■□□□□□□□□□",
        "■■□□□□□□□□",
        "■■■□□□□□□□",
        "■■■■□□□□□□",
        "■■■■■□□□□□",
        "■■■■■■□□□□",
        "■■■■■■■□□□",
        "■■■■■■■■□□",
        "■■■■■■■■■□",
        "■■■■■■■■■■",
    ]

    def __init__(self, total: int) -> None:
        self._total = total
        self._progress = 0

    @property
    def progress(self) -> int:
        return self._progress

    def update(self, chunk_len: int) -> None:
        if self._total == 0:
            return
        self._progress += chunk_len
        percentage = int(self._progress / self._total * 100)
        i = percentage // 10
        sys.stderr.write(f"\r{self._space}\r{self._bar[i]} {percentage}%")
        if i == 10:
            sys.stderr.write("\n")
        sys.stderr.flush()
