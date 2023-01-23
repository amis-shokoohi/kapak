from pathlib import Path
from typing import List

import kapak.cli.arg
from kapak.cli.pipe import Pipe
from kapak.cli.progress import Progress
from kapak.cli.password import prompt_for_password, read_password_from_file
from kapak.error import KapakError
from kapak.aes import encrypt, decrypt, BUFFER_SIZE
from kapak.version import __version__


VERSION = f"\nkapak v{__version__}\n"

DESCRIPTION = f"""
    ▄ •▄  ▄▄▄·  ▄▄▄· ▄▄▄· ▄ •▄
    █▌▄▌▪▐█ ▀█ ▐█ ▄█▐█ ▀█ █▌▄▌▪
    ▐▀▀▄·▄█▀▀█  ██▀·▄█▀▀█ ▐▀▀▄·
    ▐█.█▌▐█ ▪▐▌▐█▪·•▐█ ▪▐▌▐█.█▌    v{__version__}
    ·▀  ▀ ▀  ▀ .▀    ▀  ▀ ·▀  ▀

Description: A simple-to-use file encryption script
Repository:  https://github.com/amis-shokoohi/kapak
Help:        kapak [ -h | --help ]
"""

USAGE = """
usage: kapak [options] [command] [command options] [input]

options:
  -h, --help     Print help message
  -v, --version  Print version

commands:
  e, encrypt     Encrypt file/stdin
  d, decrypt     Decrypt file/stdin
"""

USAGE_ENCRYPT = f"""
usage: kapak [encrypt | e] [options] [input]

options:
  -h, --help           Print help message
  -o, --output         Output file path
  -p, --password-file  Password file path
  -b, --buffer-size    Buffer size in bytes (default: {BUFFER_SIZE})
"""

USAGE_DECRYPT = f"""
usage: kapak [decrypt | d] [options] [input]

options:
  -h, --help           Print help message
  -o, --output         Output file path
  -p, --password-file  Password file path
  -b, --buffer-size    Buffer size in bytes (default: {BUFFER_SIZE})
"""


def run(argv: List[str]) -> None:
    if len(argv) == 1:
        print(DESCRIPTION)
    elif argv[1] == "-h" or argv[1] == "--help":
        print(USAGE)
    elif argv[1] == "-v" or argv[1] == "--version":
        print(VERSION)
    elif argv[1] == "e" or argv[1] == "encrypt":
        arg = kapak.cli.arg.parse(argv[1:])

        if arg.help:
            print(USAGE_ENCRYPT)
            return

        password = ""
        if arg.password_file is not None:
            password = read_password_from_file(arg.password_file)
        else:
            password = prompt_for_password(confirm=True)

        total_size = 0
        if isinstance(arg.input, Path):
            _validate_path(arg.input)
            total_size = arg.input.stat().st_size

        with Pipe(arg.input, arg.output) as pipe:
            progress = Progress(total=total_size)
            for part in encrypt(pipe.src, pipe.dst, password, arg.buffer_size):
                progress.update(part)
    elif argv[1] == "d" or argv[1] == "decrypt":
        arg = kapak.cli.arg.parse(argv[1:])

        if arg.help:
            print(USAGE_DECRYPT)
            return

        password = ""
        if arg.password_file is not None:
            password = read_password_from_file(arg.password_file)
        else:
            password = prompt_for_password()

        total_size = 0
        if isinstance(arg.input, Path):
            _validate_path(arg.input)
            total_size = arg.input.stat().st_size

        with Pipe(arg.input, arg.output) as pipe:
            progress = Progress(total=total_size)
            for chunk_len in decrypt(pipe.src, pipe.dst, password, arg.buffer_size):
                progress.update(chunk_len)
    else:
        print(USAGE)


def _validate_path(p: Path) -> None:
    if not p.exists():
        raise KapakError(f"not able to find {p}")

    if not p.is_file():
        raise KapakError(f"{p} is not a file")

    if p.stat().st_size == 0:
        raise KapakError(f"{p} is empty")
