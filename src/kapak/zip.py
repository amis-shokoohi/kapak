import os
from pathlib import Path
import zipfile

from kapak.constant import TEMP_ZIP_EXT


def zip_dir(dir_path: Path) -> Path:
    changed_dir = False
    curr_dir = os.getcwd()
    # Check if dir_path is not relative to current path
    if dir_path.parent != "":
        print("hi", dir_path)
        os.chdir(dir_path.parent)
        changed_dir = True

    ff = list(Path(dir_path.name).rglob("*"))

    zf_path = dir_path.name + "." + TEMP_ZIP_EXT

    with zipfile.ZipFile(zf_path, "w") as zf:
        for f in ff:
            zf.write(f)

    zf_path_abs = Path(zf_path).resolve()

    if changed_dir:
        os.chdir(curr_dir)

    return zf_path_abs


def unzip_dir(dir_path: Path) -> Path:
    dir_path_head = os.path.split(dir_path)[0]
    with zipfile.ZipFile(dir_path, "r") as zf:
        zf.extractall(path=dir_path_head)
    return dir_path.with_suffix("")
