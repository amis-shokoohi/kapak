from pathlib import Path

import pytest

import kapak.cli.password
from kapak.error import KapakError


def test_read_password_from_file(tmp_path: Path) -> None:
    temp_file = Path(tmp_path, "temp_file")
    print(temp_file)

    with pytest.raises(KapakError, match=r"does not exist"):
        kapak.cli.password.read_password_from_file(temp_file)

    temp_file.write_text("")
    with pytest.raises(KapakError, match="password must not be empty"):
        kapak.cli.password.read_password_from_file(temp_file)

    expect = "P@ssw0rd"
    temp_file.write_text(expect)
    password = kapak.cli.password.read_password_from_file(temp_file)
    assert password == expect


def test_prompt_for_password(monkeypatch: pytest.MonkeyPatch) -> None:
    expect = ""
    monkeypatch.setattr(kapak.cli.password, "getpass", lambda msg: expect)
    with pytest.raises(KapakError, match="password must not be empty"):
        kapak.cli.password.prompt_for_password()

    expect = "P@ssw0rd"
    monkeypatch.setattr(kapak.cli.password, "getpass", lambda msg: expect)

    password = kapak.cli.password.prompt_for_password()
    assert password == expect

    password = kapak.cli.password.prompt_for_password(confirm=True)
    assert password == expect

    monkeypatch.setattr(
        kapak.cli.password,
        "getpass",
        lambda msg: "p1" if msg == "Enter password: " else "p2",
    )
    with pytest.raises(KapakError, match="passwords do not match"):
        kapak.cli.password.prompt_for_password(confirm=True)
