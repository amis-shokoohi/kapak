from kapak.constant import BUFFER_SIZE
from kapak.version import __version__


def print_description() -> None:
    print(DESCRIPTION)


def print_version() -> None:
    print(f"\nkapak v{__version__}\n")


def print_help() -> None:
    print(USAGE)


def print_help_encrypt() -> None:
    print(USAGE_ENCRYPT)


def print_help_decrypt() -> None:
    print(USAGE_DECRYPT)


DESCRIPTION = f"""
    ▄ •▄  ▄▄▄·  ▄▄▄· ▄▄▄· ▄ •▄
    █▌▄▌▪▐█ ▀█ ▐█ ▄█▐█ ▀█ █▌▄▌▪
    ▐▀▀▄·▄█▀▀█  ██▀·▄█▀▀█ ▐▀▀▄·
    ▐█.█▌▐█ ▪▐▌▐█▪·•▐█ ▪▐▌▐█.█▌    v{__version__}
    ·▀  ▀ ▀  ▀ .▀    ▀  ▀ ·▀  ▀

Description: A simple-to-use file encryption script
Link:        https://github.com/amis-shokoohi/kapak
Help:        kapak [ -h | --help ]
"""

USAGE = """
usage: kapak [global options] <command> [command options] <path>

global options:
  -h, --help     Print the help message
  -v, --version  Print the version

commands:
  e, encrypt     Encrypt the specified file/directory
  d, decrypt     Decrypt the specified file/directory
"""

USAGE_ENCRYPT = f"""
usage: kapak [encrypt | e] [options] <path>

options:
  -h, --help           Print the help message
  -b, --buffer-size    Buffer size in megabytes (default: {BUFFER_SIZE})
  -p, --password-file  Password file path (format: .txt)
"""

USAGE_DECRYPT = f"""
usage: kapak [decrypt | d] [options] <path>

options:
  -h, --help           Print the help message
  -b, --buffer-size    Buffer size in megabytes (default: {BUFFER_SIZE})
  -p, --password-file  Password file path (format: .txt)
"""
