import os
import shutil
from pathlib import Path
import argparse

from lib.file_extension import file_ext, replace_file_ext
from lib.passwd import get_password, derive_key
from lib.constants import ENCRYPT_MODE
from lib.progress_cli import ProgressCLI
import lib.encryptor
from lib.dir import zip_dir, calc_total_size, list_files

def execute(args: argparse.Namespace):
	args.buffer_size = args.buffer_size * 1024 * 1024 # ?MB
	if not os.path.exists(args.path):
		raise Exception('can not find ' + str(args.path))

	if os.path.isfile(args.path):
		encrypt_file(args.path, args.should_remove, args.buffer_size)
	elif args.should_zip and os.path.isdir(args.path):
		zip_dir_then_encrypt(args.path, args.should_remove, args.buffer_size)
	elif os.path.isdir(args.path):
		encrypt_dir(args.path, args.should_remove, args.buffer_size)
	print() # Prints new line

def encrypt_file(target_path: Path, should_remove: bool, buffer_size: int):
	if file_ext(target_path) == 'kpk':
		raise Exception('can not encrypt ' + str(target_path))

	f_out_name = replace_file_ext(target_path, 'kpk')
	if os.path.exists(f_out_name): # Overwrite error
		raise Exception(str(f_out_name) + ' already exists')

	target_size = os.stat(target_path).st_size
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')

	password = get_password(ENCRYPT_MODE)

	print('\nEncrypting...\n')
	progress = ProgressCLI(target_size)
	key, salt = derive_key(password, None)
	
	lib.encryptor.encrypt(key, salt, target_path, buffer_size, progress)

	if should_remove:
		os.remove(target_path)

def zip_dir_then_encrypt(target_path: Path, should_remove: bool, buffer_size: int):
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
	progress = ProgressCLI(target_size)
	key, salt = derive_key(password, None)

	lib.encryptor.encrypt(key, salt, zp, buffer_size, progress)
	os.remove(zp)

	if should_remove:
		shutil.rmtree(target_path)

def encrypt_dir(target_path: Path, should_remove: bool, buffer_size: int):
	password = get_password(ENCRYPT_MODE)

	print('\nLooking for files in the directory...')
	ff = list_files(target_path, ENCRYPT_MODE) # List of files in the directory
	if len(ff) == 0:
		raise Exception(str(target_path) + ' is empty')
	target_size = calc_total_size(ff)
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')
	
	print('\nEncrypting...\n')
	progress = ProgressCLI(target_size)
	key, salt = derive_key(password, None)

	for f in ff:
		f_out_name = replace_file_ext(f, 'kpk')
		if os.path.exists(f_out_name): # Overwrite error
			raise Exception(str(f_out_name) + ' already exists')
		lib.encryptor.encrypt(key, salt, f, buffer_size, progress)
		if should_remove:
			os.remove(f)