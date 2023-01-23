import io
import contextlib
import itertools

from kapak.cli.progress import Progress


def test_progress_update():
    total = 12
    progress = Progress(total)

    captured = io.StringIO()
    with contextlib.redirect_stderr(captured):
        expect = 0
        for i in itertools.repeat(2, int(total / 2)):
            expect += i
            progress.update(i)
            assert progress.progress == expect

            percentage = int(expect / total * 100)
            assert captured.getvalue().find(f"{percentage}%") != -1


def test_progress_total_zero():
    total = 0
    progress = Progress(total)

    captured = io.StringIO()
    with contextlib.redirect_stderr(captured):
        expect = 0
        for i in itertools.repeat(2, 5):
            progress.update(i)
            assert progress.progress == expect
            assert captured.getvalue() == ""
