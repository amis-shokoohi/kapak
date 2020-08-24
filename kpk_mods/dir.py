from os import path, stat
from kpk_mods.constants import ENCRYPT_MODE

def getTotalSize(fList):
	totalSize = 1
	for f in fList:
		if path.isdir(f):
			continue
		totalSize += stat(f).st_size
	return totalSize

def getFilesList(dir_path, mode):
	fList = []

	if mode == ENCRYPT_MODE:
		allFiles = list(dir_path.glob('**/*'))
		for f in allFiles:
			if path.isdir(f):
				continue
			if str(f)[-3:] != 'kpk':
				fList.append(f)
	else:
		fList = list(dir_path.glob('**/*.kpk'))

	return fList