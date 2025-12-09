import random
from pathlib import Path

import pytest

import kapak.cli.cmd
import kapak.cli.password
from kapak.error import KapakError


def test_run_print(capsys: pytest.CaptureFixture) -> None:
    cases = [
        (
            ["cmd"],
            kapak.cli.cmd.DESCRIPTION,
        ),
        (
            ["cmd", "-h"],
            kapak.cli.cmd.USAGE,
        ),
        (
            ["cmd", "--help"],
            kapak.cli.cmd.USAGE,
        ),
        (
            ["cmd", "--unknow-arg"],
            kapak.cli.cmd.USAGE,
        ),
        (
            ["cmd", "-v"],
            kapak.cli.cmd.VERSION,
        ),
        (
            ["cmd", "--version"],
            kapak.cli.cmd.VERSION,
        ),
        (
            ["cmd", "e", "-h"],
            kapak.cli.cmd.USAGE_ENCRYPT,
        ),
        (
            ["cmd", "encrypt", "--help"],
            kapak.cli.cmd.USAGE_ENCRYPT,
        ),
        (
            ["cmd", "d", "-h"],
            kapak.cli.cmd.USAGE_DECRYPT,
        ),
        (
            ["cmd", "decrypt", "--help"],
            kapak.cli.cmd.USAGE_DECRYPT,
        ),
    ]

    for input, expect in cases:
        kapak.cli.cmd.run(input)

        captured = capsys.readouterr()
        assert captured.out == expect + "\n"


def test_run_encrypt_decrypt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(kapak.cli.password, "getpass", lambda msg: "P@ssw0rd")

    temp_file1 = Path(tmp_path, "temp_file1")
    temp_file2 = Path(tmp_path, "temp_file2")
    temp_file3 = Path(tmp_path, "temp_file3")

    expect = bytes(random.getrandbits(8) for _ in range(32))
    temp_file1.write_bytes(expect)

    kapak.cli.cmd.run(
        [
            "cmd",
            "encrypt",
            "-b",
            "64",
            "-o",
            str(temp_file2),
            str(temp_file1),
        ]
    )
    kapak.cli.cmd.run(
        [
            "cmd",
            "decrypt",
            "-b",
            "64",
            "-o",
            str(temp_file3),
            str(temp_file2),
        ]
    )

    assert temp_file3.read_bytes() == expect


def test_run_encrypt_decrypt_password_file(tmp_path: Path) -> None:
    temp_file_password = Path(tmp_path, "temp_file_password")
    temp_file_password.write_text("P@ssw0rd")

    temp_file1 = Path(tmp_path, "temp_file1")
    temp_file2 = Path(tmp_path, "temp_file2")
    temp_file3 = Path(tmp_path, "temp_file3")

    expect = bytes(random.getrandbits(8) for _ in range(32))
    temp_file1.write_bytes(expect)

    kapak.cli.cmd.run(
        [
            "cmd",
            "encrypt",
            "-b",
            "64",
            "-p",
            str(temp_file_password),
            "-o",
            str(temp_file2),
            str(temp_file1),
        ]
    )
    kapak.cli.cmd.run(
        [
            "cmd",
            "decrypt",
            "-b",
            "64",
            "-p",
            str(temp_file_password),
            "-o",
            str(temp_file3),
            str(temp_file2),
        ]
    )

    assert temp_file3.read_bytes() == expect


def test_run_encrypt_path_not_exist(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(kapak.cli.password, "getpass", lambda msg: "P@ssw0rd")

    temp_file1 = Path(tmp_path, "temp_file1")
    temp_file2 = Path(tmp_path, "temp_file2")

    with pytest.raises(KapakError, match=r"not able to find"):
        kapak.cli.cmd.run(
            [
                "cmd",
                "encrypt",
                "-b",
                "64",
                "-o",
                str(temp_file2),
                str(temp_file1),
            ]
        )


def test_run_encrypt_path_not_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(kapak.cli.password, "getpass", lambda msg: "P@ssw0rd")

    temp_dir = Path(tmp_path, "temp_dir")
    temp_dir.mkdir()
    temp_file2 = Path(tmp_path, "temp_file2")

    with pytest.raises(KapakError, match=r"is not a file"):
        kapak.cli.cmd.run(
            [
                "cmd",
                "encrypt",
                "-b",
                "64",
                "-o",
                str(temp_file2),
                str(temp_dir),
            ]
        )


def test_run_encrypt_empty_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(kapak.cli.password, "getpass", lambda msg: "P@ssw0rd")

    temp_file1 = Path(tmp_path, "temp_file1")
    temp_file2 = Path(tmp_path, "temp_file2")

    temp_file1.write_bytes(b"")

    with pytest.raises(KapakError, match=r"is empty"):
        kapak.cli.cmd.run(
            [
                "cmd",
                "encrypt",
                "-b",
                "64",
                "-o",
                str(temp_file2),
                str(temp_file1),
            ]
        )
