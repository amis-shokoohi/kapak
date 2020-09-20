from os import path, stat

from kpk_mods.constants import ENCRYPT_MODE
from kpk_mods.file_exntension import fileExt

def calcTotalSize(files):
	totalSize = 1
	for f in files:
		if path.isfile(f):
			totalSize += stat(f).st_size
	return totalSize

def files(dir_path, mode):
	if mode == ENCRYPT_MODE:
		files = []
		allFiles = list(dir_path.glob('**/*'))
		for f in allFiles:
			if path.isfile(f) and fileExt(f) != 'kpk':
				files.append(f)
		return files

	return list(dir_path.glob('**/*.kpk'))