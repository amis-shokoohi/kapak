import sys


class Logger:
    def info(self, msg: str, end: str = "\n") -> None:
        sys.stdout.write(msg + end)
        sys.stdout.flush()
