import os
from pathlib import Path
import argparse

from lib.message import print_help_decrypt
from lib.file_exntension import file_ext
from lib.passwd import get_password
from lib.constants import DECRYPT_MODE, TEMP_ZIP_EXT
from lib.progress import Progress
import lib.decryptor
from lib.dir import unzip_dir, calc_total_size, list_files

def execute(argv: [str]):
	if len(argv) == 2 or argv[2] == '-h' or argv[2] == '--help':
		print_help_decrypt()
		return

	parser = argparse.ArgumentParser(prog='kapak', add_help=False)
	subparser = parser.add_subparsers()
	subparser_decrypt_cmd = subparser.add_parser('decrypt', add_help=False)
	subparser_decrypt_cmd.add_argument('-r', '--remove', action='store_true', dest='should_remove')
	subparser_decrypt_cmd.add_argument('path', type=Path)
	args = subparser_decrypt_cmd.parse_args(args=argv[2:])

	if not os.path.exists(args.path):
		raise Exception('can not find ' + str(args.path))

	if os.path.isfile(args.path):
		decrypt_file(args.path, args.should_remove)
	elif os.path.isdir(args.path):
		decrypt_dir(args.path, args.should_remove)

def decrypt_file(target_path: Path, should_remove: bool):
	if file_ext(target_path) != 'kpk':
			raise Exception('can not decrypt ' + str(target_path))

	target_size = os.stat(target_path).st_size
	if target_size == 0:
		raise Exception(str(target_path) + ' is empty')

	password = get_password(DECRYPT_MODE)		

	print('\nDecrypting...\n')
	progress = Progress()
	progress.set_total_size(target_size)
	f_out_path, f_out_ext = lib.decryptor.decrypt(password, target_path)
	if f_out_ext == TEMP_ZIP_EXT:
		unzip_dir(f_out_path)
		os.remove(f_out_path)

	if should_remove:
		os.remove(target_path)

def decrypt_dir(target_path: Path, should_remove: bool):
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
		_, _ = lib.decryptor.decrypt(password, f)
		if should_remove:
			os.remove(f)