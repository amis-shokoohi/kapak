import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List

from kapak.aes import BUFFER_SIZE


@dataclass
class SubCmdArg:
    help: bool = False
    password_file: Optional[Path] = None
    buffer_size: int = BUFFER_SIZE
    output: Optional[Path] = None
    input: Optional[Path] = None


def parse(argv: List[str]) -> SubCmdArg:
    if len(argv) >= 2 and (argv[1] == "-h" or argv[1] == "--help"):
        return SubCmdArg(help=True)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-p", "--password-file", nargs="?", type=Path, dest="password_file"
    )
    parser.add_argument(
        "-b",
        "--buffer-size",
        nargs="?",
        type=int,
        default=BUFFER_SIZE,
        dest="buffer_size",
    )
    parser.add_argument("-o", "--output", nargs="?", type=Path, dest="output")
    parser.add_argument("input", nargs="?", type=Path)
    arg, unknown_arg = parser.parse_known_args(args=argv[1:])

    if len(unknown_arg):
        return SubCmdArg(help=True)

    return SubCmdArg(
        password_file=arg.password_file,
        buffer_size=arg.buffer_size,
        output=arg.output,
        input=arg.input,
    )
