import sys

from kapak.cli.cmd import run
from kapak.error import KapakError


COLOR_RED = "\033[0;31m"
COLOR_NONE = "\033[0m"


def main() -> None:
    try:
        run(sys.argv)
    except KeyboardInterrupt:
        sys.exit(1)
    except KapakError as err:
        sys.stderr.write(f"\n{COLOR_RED}[ERROR] {err.args[0]}{COLOR_NONE}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
