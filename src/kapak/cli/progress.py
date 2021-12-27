from math import ceil, floor

from kapak.logger import LoggerType


class Progress:
    _bar = [
        "[□□□□□□□□□□]",
        "[■□□□□□□□□□]",
        "[■■□□□□□□□□]",
        "[■■■□□□□□□□]",
        "[■■■■□□□□□□]",
        "[■■■■■□□□□□]",
        "[■■■■■■□□□□]",
        "[■■■■■■■□□□]",
        "[■■■■■■■■□□]",
        "[■■■■■■■■■□]",
        "[■■■■■■■■■■]",
    ]

    def __init__(self, logger: LoggerType) -> None:
        self._logger = logger
        self._progress = 0

    def set_total(self, total: int) -> None:
        self._total = total
        self._progress = 0  # Reset

    def update(self, part: int) -> None:
        self._progress += part
        percentage = ceil(self._progress / self._total * 100)
        percentage = percentage if percentage <= 100 else 100
        i = floor(percentage / 10)
        space = 20 * " "
        self._logger.info(f"\r{space}\r{self._bar[i]} {percentage}%", end="")
