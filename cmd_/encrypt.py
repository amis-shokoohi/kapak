import os
import shutil

from lib.message import print_help_encrypt
from lib.argparse import has_remove_flag, has_zip_flag, get_path
from lib.file_exntension import file_ext
from lib.passwd import get_password, derive_key
from lib.constants import ENCRYPT_MODE
from lib.progress import Progress
from lib.encryption import FileEncryptor
from lib.file_exntension import replace_file_ext
from lib.dir import zip_dir, calc_total_size, list_files

def execute(argv):
	if len(argv) == 2 or argv[2] == '-h' or argv[2] == '--help':
		print_help_encrypt()
		return

	should_remove = True if has_remove_flag(argv[2:]) else False
	should_zip = True if has_zip_flag(argv[2:]) else False

	target_path = get_path(argv[2:])
	if target_path == None:
		raise Exception('PATH is not specified')
	if not os.path.exists(target_path):
		raise Exception('can not find ' + str(target_path))

	if os.path.isfile(target_path):
		if file_ext(target_path) == 'kpk':
			raise Exception('can not encrypt ' + str(target_path))
		f_out_name = replace_file_ext(target_path, 'kpk')
		if os.path.exists(f_out_name): # Overwrite error
			raise Exception(f_out_name + ' already exists')
		target_size = os.stat(target_path).st_size
		if target_size == 0:
			raise Exception(str(target_path) + ' is empty')

		password = get_password(ENCRYPT_MODE)

		print('\nEncrypting...\n')
		progress = Progress()
		progress.set_total_size(target_size)
		key, salt = derive_key(password, None)
		encryptor = FileEncryptor(key, salt, target_path)
		encryptor.encrypt()
		if should_remove:
			os.remove(target_path)
		print('\r' + 20*' ' + '\r[■■■■■■■■■■] 100%\n') # TODO: This is a hack, should be fixed in lib/progress.py
		return

	if should_zip and os.path.isdir(target_path):
		f_out_name = str(target_path) + '.kpk'
		if os.path.exists(f_out_name): # Overwrite error
			raise Exception(f_out_name + ' already exists')

		password = get_password(ENCRYPT_MODE)

		print('\nZipping...')
		zp = zip_dir(target_path) # Creates a temporary zip file
		target_size = os.stat(zp).st_size
		if target_size == 0:
			raise Exception(str(target_path) + ' is empty')

		print('\nEncrypting...\n')
		progress = Progress()
		progress.set_total_size(target_size)
		key, salt = derive_key(password, None)
		encryptor = FileEncryptor(key, salt, zp)
		encryptor.encrypt()
		os.remove(zp)
		if should_remove:
			shutil.rmtree(target_path)
		return

	if os.path.isdir(target_path):
		password = get_password(ENCRYPT_MODE)

		print('\nLooking for files in the directory...')
		ff = list_files(target_path, ENCRYPT_MODE) # List of files in the directory
		if len(ff) == 0:
			raise Exception(str(target_path) + ' is empty')
		target_size = calc_total_size(ff)
		if target_size == 0:
			raise Exception(str(target_path) + ' is empty')
		
		print('\nEncrypting...\n')
		progress = Progress()
		progress.set_total_size(target_size)
		key, salt = derive_key(password, None)
		for f in ff:
			f_out_name = replace_file_ext(f, 'kpk')
			if os.path.exists(f_out_name): # Overwrite error
				raise Exception(f_out_name + ' already exists')
			encryptor = FileEncryptor(key, salt, f)
			encryptor.encrypt()
			if should_remove:
				os.remove(f)
		print('\r' + 20*' ' + '\r[■■■■■■■■■■] 100%\n') # TODO: This is a hack, should be fixed in lib/progress.py
		