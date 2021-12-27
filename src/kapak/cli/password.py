import sys
from pathlib import Path
from getpass import getpass

from kapak.error import KapakError


MIN_PASS_LEN = 3
MAX_PASS_LEN = 1024


def read_pass_from_file(password_file: Path) -> str:
    if not password_file.exists():
        raise KapakError(f"{password_file} doest not exist")

    if not password_file.match("*.txt"):
        raise KapakError("password file must be a text (.txt) file")

    password = password_file.read_text(encoding="utf-8").rstrip()

    if not MIN_PASS_LEN < len(password) < MAX_PASS_LEN:
        raise KapakError(
            f"password must be between {MIN_PASS_LEN} to {MAX_PASS_LEN} characters"
        )

    # Remove password file
    password_file.unlink()

    return password


def read_pass_from_stdin(confirm: bool) -> str:
    password = ""
    valid_password = False
    while not valid_password:
        password = _ask_pass(confirm)
        if not MIN_PASS_LEN < len(password) < MAX_PASS_LEN:
            _print_error(
                f"password must be between {MIN_PASS_LEN} to {MAX_PASS_LEN} characters"
            )
            continue
        valid_password = True
    return password


def _ask_pass(confirm: bool) -> str:
    p1 = getpass("Enter password: ")
    if confirm:
        p2 = getpass("Reenter password: ")
        if p2 != p1:
            _print_error("passwords do not match")
            return _ask_pass(True)
    return p1


def _print_error(msg: str) -> None:
    sys.stderr.write(f"[ERROR] {msg}\n")
