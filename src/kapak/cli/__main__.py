import sys
import argparse
from pathlib import Path
from typing import List

from kapak.constant import BUFFER_SIZE
from kapak.encryptor import Encryptor
from kapak.decryptor import Decryptor
from kapak.error import KapakError
import kapak.cli.message
from kapak.cli.password import read_pass_from_stdin, read_pass_from_file
from kapak.cli.logger import Logger
from kapak.cli.progress import Progress


def cli(argv: List[str]) -> None:
    if len(argv) == 1:
        kapak.cli.message.print_description()
    elif argv[1] == "-h" or argv[1] == "--help":
        kapak.cli.message.print_help()
    elif argv[1] == "-v" or argv[1] == "--version":
        kapak.cli.message.print_version()
    elif argv[1] == "e" or argv[1] == "encrypt":
        if len(argv) == 2 or argv[2] == "-h" or argv[2] == "--help":
            kapak.cli.message.print_help_encrypt()
            return
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-b",
            "--buffer-size",
            nargs="?",
            type=int,
            default=BUFFER_SIZE,
            dest="buffer_size",
        )
        parser.add_argument(
            "-p", "--password-file", nargs="?", type=Path, dest="password_file"
        )
        parser.add_argument("path", type=Path)
        args = parser.parse_args(args=argv[2:])

        password = ""
        if args.password_file is not None:
            password = read_pass_from_file(args.password_file)
        else:
            password = read_pass_from_stdin(confirm=True)

        logger = Logger()
        progress = Progress(logger)

        e = Encryptor(buffer_size=args.buffer_size, logger=logger, progress=progress)
        e.encrypt(src=args.path, password=password)
        print()  # Print a newline
    elif argv[1] == "d" or argv[1] == "decrypt":
        if len(argv) == 2 or argv[2] == "-h" or argv[2] == "--help":
            kapak.cli.message.print_help_decrypt()
            return
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-b",
            "--buffer-size",
            nargs="?",
            type=int,
            default=BUFFER_SIZE,
            dest="buffer_size",
        )
        parser.add_argument(
            "-p", "--password-file", nargs="?", type=Path, dest="password_file"
        )
        parser.add_argument("path", type=Path)
        args = parser.parse_args(args=argv[2:])

        password = ""
        if args.password_file is not None:
            password = read_pass_from_file(args.password_file)
        else:
            password = read_pass_from_stdin(confirm=False)

        logger = Logger()
        progress = Progress(logger)

        d = Decryptor(buffer_size=args.buffer_size, logger=logger, progress=progress)
        d.decrypt(src=args.path, password=password)
        print()  # Print a newline
    else:
        kapak.cli.message.print_help()


def main() -> None:
    try:
        cli(sys.argv)
    except KeyboardInterrupt:
        sys.exit()
    except KapakError as err:
        sys.stderr.write(f"\n[ERROR] {err.args[0]}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
