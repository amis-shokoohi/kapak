import shutil
from pathlib import Path

from lib.file_extension import replace_file_ext
from lib.passwd import get_password
from lib.key import derive_key
from lib.constants import ENCRYPT_MODE
from lib.progress import Progress
import lib.encryptor
from lib.dir import zip_dir, calc_total_size, contains_encrypted_files

def execute(path: Path, buffer_size: int, should_remove: bool, should_zip: bool):
	buffer_size = buffer_size * 1024 * 1024 # ?MB
	if not path.exists():
		raise Exception('can not find ' + str(path))

	if path.is_file():
		encrypt_file(path, should_remove, buffer_size)
	elif should_zip and path.is_dir():
		zip_dir_then_encrypt(path, should_remove, buffer_size)
	elif path.is_dir():
		encrypt_dir(path, should_remove, buffer_size)
	print() # Prints new line

def encrypt_file(target_path: Path, should_remove: bool, buffer_size: int):
	target_size = target_path.stat().st_size
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')

	f_out_name = replace_file_ext(target_path, 'kpk')
	if f_out_name.exists(): # Overwrite error
		raise Exception(str(f_out_name) + ' already exists')

	password = get_password(ENCRYPT_MODE)
	key, salt = derive_key(password, None)

	print('\nEncrypting...\n')
	progress = Progress(target_size)
	lib.encryptor.encrypt(target_path, key, salt, buffer_size, progress)

	if should_remove:
		target_path.unlink()

def zip_dir_then_encrypt(target_path: Path, should_remove: bool, buffer_size: int):
	f_out_name = Path(str(target_path) + '.kpk')
	if f_out_name.exists(): # Overwrite error
		raise Exception(str(f_out_name) + ' already exists')

	password = get_password(ENCRYPT_MODE)
	key, salt = derive_key(password, None)

	print('\nLooking for files in the directory...')
	if contains_encrypted_files(target_path):
		raise Exception(str(target_path) + ' contains encrypted files')

	print('\nZipping...')
	zp = zip_dir(target_path) # Creates a temporary zip file
	target_size = zp.stat().st_size
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')

	print('\nEncrypting...\n')
	progress = Progress(target_size)
	lib.encryptor.encrypt(zp, key, salt, buffer_size, progress)

	zp.unlink()
	if should_remove:
		shutil.rmtree(target_path)

def encrypt_dir(target_path: Path, should_remove: bool, buffer_size: int):
	password = get_password(ENCRYPT_MODE)
	key, salt = derive_key(password, None)

	print('\nLooking for files in the directory...')
	if contains_encrypted_files(target_path):
		raise Exception(str(target_path) + ' contains encrypted files')
	ff = [f for f in target_path.rglob('*') 
	      if f.is_file() and f.stat().st_size != 0]
	if len(ff) == 0:
		raise Exception(str(target_path) + ' is empty')
	target_size = calc_total_size(ff)
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')

	print('\nEncrypting...\n')
	progress = Progress(target_size)
	for f in ff:
		lib.encryptor.encrypt(f, key, salt, buffer_size, progress)
		if should_remove:
			f.unlink()