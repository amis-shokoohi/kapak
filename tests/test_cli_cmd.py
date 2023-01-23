import io
import contextlib

import kapak.cli.cmd


def test_run_print() -> None:
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

    for (input, expect) in cases:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            kapak.cli.cmd.run(input)
            assert captured.getvalue() == expect + "\n"
