import os

from lib.message import print_help_decrypt
from lib.argparse import has_remove_flag, get_path
from lib.file_exntension import file_ext
from lib.passwd import get_password
from lib.constants import DECRYPT_MODE, TEMP_ZIP_EXT
from lib.progress import Progress
from lib.decryptor import FileDecryptor
from lib.dir import unzip_dir, calc_total_size, list_files

def execute(argv):
	if len(argv) == 2 or argv[2] == '-h' or argv[2] == '--help':
		print_help_decrypt()
		return

	should_remove = True if has_remove_flag(argv[2:]) else False

	target_path = get_path(argv[2:])
	if target_path == None:
		raise Exception('PATH is not specified')
	if not os.path.exists(target_path):
		raise Exception('can not find ' + str(target_path))

	if os.path.isfile(target_path):
		if file_ext(target_path) != 'kpk':
			raise Exception('can not decrypt ' + str(target_path))
		target_size = os.stat(target_path).st_size
		if target_size == 0:
			raise Exception(str(target_path) + ' is empty')

		password = get_password(DECRYPT_MODE)		

		print('\nDecrypting...\n')
		progress = Progress()
		progress.set_total_size(target_size)
		decryptor = FileDecryptor(password, target_path)
		decryptor.decrypt()
		if decryptor.get_file_ext() == TEMP_ZIP_EXT:
			unzip_dir(decryptor.get_file_name())
			os.remove(decryptor.get_file_name())
		if should_remove:
			os.remove(target_path)
		print('\r' + 20*' ' + '\r[■■■■■■■■■■] 100%\n') # TODO: This is a hack, should be fixed in lib/progress.py
		return

	if os.path.isdir(target_path):
		password = get_password(DECRYPT_MODE)		

		print('\nDecrypting...\n')
		ff = list_files(target_path, DECRYPT_MODE) # List of files in the directory
		if len(ff) == 0:
			raise Exception(str(target_path) + ' is empty')
		target_size = calc_total_size(ff)
		if target_size == 0:
			raise Exception(str(target_path) + ' is empty')
		progress = Progress()
		progress.set_total_size(target_size)
		for f in ff:
			decryptor = FileDecryptor(password, f)
			decryptor.decrypt()
			if should_remove:
				os.remove(f)
		print('\r' + 20*' ' + '\r[■■■■■■■■■■] 100%\n') # TODO: This is a hack, should be fixed in lib/progress.py
