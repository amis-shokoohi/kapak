from sys import argv
from pathlib import Path

from lib.constants import ENCRYPT_MODE, DECRYPT_MODE, USAGE

def hasFlag(flag_name, argv, arg_count_min, arg_count_max):
	flag_exists = False
	flag_count = 0
	l = len(argv)
	if l >= arg_count_min or l <= arg_count_max:
		for v in argv[1:]:
			if v == '-'+flag_name[0] or v == '--'+flag_name:
				flag_exists = True
				flag_count += 1

		if flag_count > 1:
			raise Exception(USAGE)

	return flag_exists

def hasRemoveFlag(argv):
	return hasFlag('remove', argv, 4, 5)

def hasZipFlag(argv):
	return hasFlag('zip', argv, 4, 5)

def whichMode(argv):
	e = hasFlag('encrypt', argv, 3, 4)
	d = hasFlag('decrypt', argv, 3, 5)
	if not e ^ d:
		raise Exception(USAGE)
	return ENCRYPT_MODE if e else DECRYPT_MODE

def getPath(agrv):
	l = len(argv)
	if l >= 3 or l <= 5:
		for v in argv[1:]:
			if v[0:1] != '-':
				return Path(v)
	return None