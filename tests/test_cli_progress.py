import itertools

import pytest

from kapak.cli.progress import Progress


def test_progress_update(capsys: pytest.CaptureFixture) -> None:
    total = 12
    progress = Progress(total)

    expect = 0
    for i in itertools.repeat(2, int(total / 2)):
        expect += i
        progress.update(i)
        assert progress.progress == expect

        percentage = int(expect / total * 100)

        captured = capsys.readouterr()
        assert captured.err.find(f"{percentage}%") != -1


def test_progress_total_zero(capsys: pytest.CaptureFixture) -> None:
    total = 0
    progress = Progress(total)

    expect = 0
    for i in itertools.repeat(2, 5):
        progress.update(i)
        assert progress.progress == expect

        captured = capsys.readouterr()
        assert captured.out == ""
