import io
import sys
import random
from pathlib import Path
from dataclasses import dataclass
from typing import BinaryIO

import pytest

from kapak.cli.pipe import Pipe


@dataclass(frozen=True)
class FakeStdIn:
    buffer: BinaryIO


def test_pipe_filein_fileout(tmp_path: Path) -> None:
    temp_filein = Path(tmp_path, "temp_filein")
    temp_fileout = Path(tmp_path, "temp_fileout")

    expect = bytes(random.getrandbits(8) for _ in range(32))
    temp_filein.write_bytes(expect)

    with Pipe(temp_filein, temp_fileout) as pipe:
        assert pipe.src_is_file is True
        assert pipe.dst_is_file is True

        pipe.dst.write(pipe.src.read())

    assert temp_fileout.read_bytes() == expect


def test_pipe_stdin_stdout(
    monkeypatch: pytest.MonkeyPatch, capsysbinary: pytest.CaptureFixture
) -> None:
    expect = bytes(random.getrandbits(8) for _ in range(32))

    monkeypatch.setattr(sys, "stdin", FakeStdIn(buffer=io.BytesIO(expect)))

    with Pipe(None, None) as pipe:
        assert pipe.src_is_file is False
        assert pipe.dst_is_file is False

        pipe.dst.write(pipe.src.read())

    captured = capsysbinary.readouterr()
    assert captured.out == expect
