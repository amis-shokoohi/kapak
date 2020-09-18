from os import path, stat
from kpk_mods.constants import ENCRYPT_MODE

def getTotalSize(fList):
	totalSize = 1
	for f in fList:
		if not path.isdir(f):
			totalSize += stat(f).st_size
	return totalSize

def getFiles(dir_path, mode):
	if mode == ENCRYPT_MODE:
		files = []
		allFiles = list(dir_path.glob('**/*'))
		for f in allFiles:
			if not path.isdir(f) and str(f)[-3:] != 'kpk':
				files.append(f)
		return files

	return list(dir_path.glob('**/*.kpk'))