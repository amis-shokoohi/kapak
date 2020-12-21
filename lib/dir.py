import os
import pathlib
import zipfile

from lib.constants import ENCRYPT_MODE, TEMP_ZIP_EXT
from lib.file_exntension import fileExt

def calcTotalSize(files):
	totalSize = 1
	for f in files:
		if os.path.isfile(f):
			totalSize += os.stat(f).st_size
	return totalSize

def files(dir_path, mode):
	if mode == ENCRYPT_MODE:
		files = []
		allFiles = list(dir_path.glob('**/*'))
		for f in allFiles:
			if os.path.isfile(f) and fileExt(f) != 'kpk':
				files.append(f)
		return files

	return list(dir_path.glob('**/*.kpk'))

def zipDir(dir_path):
	ff = list(dir_path.glob('**/*'))
	zp = pathlib.Path(
		os.path.split(dir_path.resolve())[0],
		dir_path.name+'.'+TEMP_ZIP_EXT
	)
	with zipfile.ZipFile(zp, 'w') as zf:
		for f in ff:
			zf.write(f)
	return zp

def unzipDir(dir_path):
	with zipfile.ZipFile(dir_path, 'r') as zf:
		zf.extractall()