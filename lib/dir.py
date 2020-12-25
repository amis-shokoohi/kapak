import os
import pathlib
import zipfile

from lib.constants import DECRYPT_MODE, TEMP_ZIP_EXT
from lib.file_exntension import file_ext

def calc_total_size(files):
	total_size = 0
	for f in files:
		total_size += os.stat(f).st_size
	return total_size

def list_files(dir_path, mode):
	if mode == DECRYPT_MODE:
		return list(dir_path.glob('**/*.kpk'))

	file_list = []
	all_files = list(dir_path.glob('**/*'))
	for f in all_files:
		if os.path.isfile(f) and file_ext(f) != 'kpk':
			file_list.append(f)
	return file_list


def zip_dir(dir_path):
	ff = list(dir_path.glob('**/*'))
	zp = pathlib.Path(
		os.path.split(dir_path.resolve())[0],
		dir_path.name+'.'+TEMP_ZIP_EXT
	)
	with zipfile.ZipFile(zp, 'w') as zf:
		for f in ff:
			zf.write(f)
	return zp

def unzip_dir(dir_path):
	with zipfile.ZipFile(dir_path, 'r') as zf:
		zf.extractall()