import re

from lib.constants import ENCRYPT_MODE, DECRYPT_MODE

def fileExt(f_path):
	p = re.compile('\.([\w]+)$')
	match = p.search(str(f_path))
	if match == None:
		return ''
	return match.group(1)

def replaceFileExt(f_path, new_ext):
	p = re.compile('\.[\w]+$')
	match = p.search(str(f_path))
	if match == None:
		return str(f_path) + '.' + new_ext
	return p.sub('.' + new_ext, str(f_path))

def validateFileByExt(f_path, mode):
	if mode == ENCRYPT_MODE and fileExt(f_path) == 'kpk':
		raise Exception('\n Error: Can NOT encrypt ' + str(f_path) + '\n')
	if mode == DECRYPT_MODE and fileExt(f_path) != 'kpk':
		raise Exception('\n Error: Can NOT decrypt ' + str(f_path) + '\n')