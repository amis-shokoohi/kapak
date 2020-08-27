from sys import argv

from kpk_mods.constants import ENCRYPT_MODE, DECRYPT_MODE

def hasRemoveFlag(argv):
	rm_flag = False
	flag_count = 0
	if len(argv) == 4:
		for v in argv[1:]:
			if v == '-r' or v == '--remove':
				rm_flag = True
				flag_count += 1

		if flag_count < 1 or flag_count > 2:
			exit('\n Error: Incorrect remove flag\n')

	return rm_flag

def whichMode(argv):
	mode_flag = None
	flag_count = 0
	if len(argv) == 3 or len(argv) == 4:
		for v in argv[1:]:
			if v == '-e' or v == '--encrypt':
				mode_flag = ENCRYPT_MODE
				flag_count += 1
			elif v == '-d' or v == '--decrypt':
				mode_flag = DECRYPT_MODE
				flag_count += 1

		if flag_count > 1:
			mode_flag = None

	return mode_flag

def getPath(agrv):
	if len(argv) == 3 or len(argv) == 4:
		for v in argv[1:]:
			if v[0:1] != '-':
				return v
	return None