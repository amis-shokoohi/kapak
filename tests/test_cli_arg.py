from pathlib import Path

from kapak.cli.arg import parse, SubCmdArg


def test_parse() -> None:
    cases = [
        (
            ["subcmd", "-h"],
            SubCmdArg(help=True),
        ),
        (
            ["subcmd", "--help"],
            SubCmdArg(help=True),
        ),
        (
            ["subcmd", "-p", "p.txt", "-b", "1024"],
            SubCmdArg(password_file=Path("p.txt"), buffer_size=1024),
        ),
        (
            ["subcmd", "--password-file", "p.txt", "--buffer-size", "1024"],
            SubCmdArg(password_file=Path("p.txt"), buffer_size=1024),
        ),
        (
            ["subcmd", "in"],
            SubCmdArg(input=Path("in")),
        ),
        (
            ["subcmd", "-o", "out"],
            SubCmdArg(output=Path("out")),
        ),
        (
            ["subcmd", "--output", "out"],
            SubCmdArg(output=Path("out")),
        ),
        (
            ["subcmd", "-o", "out", "in"],
            SubCmdArg(input=Path("in"), output=Path("out")),
        ),
        (
            ["subcmd", "--unknown-arg"],
            SubCmdArg(help=True),
        ),
    ]

    for (input, expect) in cases:
        assert parse(input) == expect
