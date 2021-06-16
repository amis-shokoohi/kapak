from pathlib import Path

from lib.file_extension import file_ext
from lib.passwd import get_password
from lib.constants import TEMP_ZIP_EXT
from lib.progress import Progress
import lib.decryptor
from lib.dir import unzip_dir, calc_total_size

def execute(path: Path, buffer_size: int, should_remove: bool):
	buffer_size = buffer_size * 1024 * 1024 # ?MB
	if not path.exists():
		raise Exception('can not find ' + str(path))

	if path.is_file():
		decrypt_file(path, should_remove, buffer_size)
	elif path.is_dir():
		decrypt_dir(path, should_remove, buffer_size)
	print() # Prints new line

def decrypt_file(target_path: Path, should_remove: bool, buffer_size: int):
	if file_ext(target_path) != 'kpk':
		raise Exception('can not decrypt ' + str(target_path))

	target_size = target_path.stat().st_size
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')

	password = get_password(confirm=False)

	print('\nDecrypting...\n')
	progress = Progress(target_size)
	f_out_path, f_out_ext = lib.decryptor.decrypt(target_path, password, buffer_size, progress)
	if f_out_ext == TEMP_ZIP_EXT:
		unzip_dir(f_out_path)
		f_out_path.unlink()

	if should_remove:
		target_path.unlink()

def decrypt_dir(target_path: Path, should_remove: bool, buffer_size: int):
	password = get_password(confirm=False)

	print('\nDecrypting...\n')
	ff = list(target_path.rglob('*.kpk'))
	if len(ff) == 0:
		raise Exception(str(target_path) + ' is empty')

	target_size = calc_total_size(ff)
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')

	progress = Progress(target_size)
	for f in ff:
		_, _ = lib.decryptor.decrypt(f, password, buffer_size, progress)
		if should_remove:
			f.unlink()