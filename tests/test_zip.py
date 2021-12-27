import os
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import Generator, List

import pytest
from pytest_unordered import unordered  # type: ignore

from kapak.zip import zip_dir, unzip_dir


@pytest.fixture
def tmp_dir() -> Generator[Path, None, None]:
    # Setup
    parent = Path(tempfile.mkdtemp())
    tmp_dir_ = Path(parent, "tmp_dir")
    tmp_dir_.mkdir()
    data = b"abcdefghijklmnopqrstuvwxyz0123456789"  # 36B
    for i in range(3):
        f = Path(tmp_dir_, str(i))
        f.write_bytes(data)

    yield tmp_dir_

    # Teardown
    shutil.rmtree(parent)


def test_zip_dir(tmp_dir: Path) -> None:
    zf_path = zip_dir(tmp_dir)
    assert zipfile.is_zipfile(zf_path)
    assert zf_path.parent == tmp_dir.parent

    zff: List[Path] = []
    with zipfile.ZipFile(zf_path, mode="r") as zf:
        zff = [Path(f) for f in zf.namelist()]
    assert zff == unordered([f.relative_to(tmp_dir.parent) for f in tmp_dir.glob("*")])


@pytest.fixture
def tmp_dir_here() -> Generator[Path, None, None]:
    # Setup
    curr_dir = os.getcwd()
    parent = Path(Path(tempfile.mkdtemp(dir=curr_dir)).name)
    tmp_dir_ = Path(parent, "tmp_dir")
    tmp_dir_.mkdir()
    data = b"abcdefghijklmnopqrstuvwxyz0123456789"  # 36B
    for i in range(3):
        f = Path(tmp_dir_, str(i))
        f.write_bytes(data)

    yield tmp_dir_

    # Teardown
    shutil.rmtree(parent)


def test_zip_dir_here(tmp_dir_here: Path) -> None:
    zf_path = zip_dir(tmp_dir_here)
    assert zipfile.is_zipfile(zf_path)
    assert zf_path.parent == tmp_dir_here.resolve().parent

    zff: List[Path] = []
    with zipfile.ZipFile(zf_path, mode="r") as zf:
        zff = [Path(f) for f in zf.namelist()]
    assert zff == unordered(
        [f.relative_to(tmp_dir_here.parent) for f in tmp_dir_here.glob("*")]
    )


@pytest.fixture
def tmp_zip_file() -> Generator[Path, None, None]:
    # Setup
    parent = Path(tempfile.mkdtemp())
    tmp_dir_ = Path(parent, "tmp_dir")
    tmp_dir_.mkdir()
    data = b"abcdefghijklmnopqrstuvwxyz0123456789"  # 36B
    for i in range(3):
        f = Path(tmp_dir_, str(i))
        f.write_bytes(data)
    zf_path = zip_dir(tmp_dir_)
    shutil.rmtree(tmp_dir_)

    yield zf_path

    # Teardown
    shutil.rmtree(parent)


def test_unzip_dir(tmp_zip_file: Path) -> None:
    dir_path = unzip_dir(tmp_zip_file)
    assert dir_path.is_dir()
    assert dir_path.parent == tmp_zip_file.parent

    zff: List[Path] = []
    with zipfile.ZipFile(tmp_zip_file, mode="r") as zf:
        zff = [Path(f) for f in zf.namelist()]
    assert [f.relative_to(dir_path.parent) for f in dir_path.glob("*")] == unordered(
        zff
    )
