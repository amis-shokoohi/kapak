from pathlib import Path
from getpass import getpass

from kapak.error import KapakError


def read_password_from_file(password_file: Path) -> str:
    if not password_file.exists():
        raise KapakError(f"{password_file} does not exist")
    p = password_file.read_text(encoding="utf-8").rstrip()
    _validate_password(p)
    return p


def prompt_for_password(confirm: bool = False) -> str:
    p = getpass("Enter password: ")
    _validate_password(p)
    if confirm and getpass("Confirm password: ") != p:
        raise KapakError("passwords do not match")
    return p


def _validate_password(p: str) -> None:
    if len(p) == 0:
        raise KapakError("password must not be empty")
