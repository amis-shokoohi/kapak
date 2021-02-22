import os
from pathlib import Path
import zipfile

from lib.constants import DECRYPT_MODE, TEMP_ZIP_EXT
from lib.file_extension import file_ext

def calc_total_size(files: [Path]) -> int:
	total_size = 0
	for f in files:
		total_size += os.stat(f).st_size
	return total_size

def list_files(dir_path: Path, mode: int) -> [Path]:
	if mode == DECRYPT_MODE:
		return list(dir_path.rglob('*.kpk'))
	return list(filter(
		lambda f: os.path.isfile(f) and file_ext(f) != 'kpk',
		list(dir_path.rglob('*'))
	))

def zip_dir(dir_path: Path) -> Path:
	splitted = os.path.split(dir_path)
	dir_path_head = splitted[0]
	dir_path_rel = Path(splitted[1])

	changed_dir = False
	curr_dir = os.getcwd()
	if dir_path_head != '':
		os.chdir(dir_path_head)
		changed_dir = True

	ff = list(dir_path_rel.rglob('*'))

	zp = dir_path_rel.name+'.'+TEMP_ZIP_EXT

	with zipfile.ZipFile(zp, 'w') as zf:
		for f in ff:
			zf.write(f)

	zp_abs = Path(zp).resolve()

	if changed_dir:
		os.chdir(curr_dir)

	return zp_abs

def unzip_dir(dir_path: Path):
	dir_path_head = os.path.split(dir_path)[0]
	with zipfile.ZipFile(dir_path, 'r') as zf:
		zf.extractall(path=dir_path_head)