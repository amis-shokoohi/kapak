import os
from sys import argv, exit
from pathlib import Path

from lib.arg_parse import hasRemoveFlag, whichMode, getPath
from lib.passwd import getPassword, deriveKey
from lib.decryption import Decryptor
from lib.encryption import Encryptor
from lib.message import printDescription, printHelp, printUsage
from lib.dir import files, calcTotalSize
from lib.constants import ENCRYPT_MODE
from lib.file_exntension import validateFileByExt

def start():
	# Usage message
	if len(argv) == 1:
		printDescription()
		return

	# Help message
	if argv[1] == '-h' or argv[1] == '--help':
		printHelp()
		return

	# Check for [-r] or [--remove] flag
	rm = hasRemoveFlag(argv)

	mode = whichMode(argv)
	if mode == None:
		printUsage()
		return
		
	target_path = Path(getPath(argv))
	if target_path == None:
		raise Exception('\n Error: <path> variable NOT specified\n')
	elif not os.path.exists(target_path):
		raise Exception('\n Error: Can NOT find ' + str(target_path) + '\n')

	if os.path.isfile(target_path):
		validateFileByExt(target_path, mode)

		password = getPassword(mode)
		
		target_size = os.stat(target_path).st_size

		if mode == ENCRYPT_MODE:
			print('\n Encrypting...\n')
			(key, salt) = deriveKey(password, None)
			encryptor = Encryptor(key, salt, target_path)
			encryptor.encryptFile(target_size)
			if rm:
				os.remove(target_path)
			print('\r' + 20*' ' + '\r [■■■■■■■■■■] 100%') # TODO: This is a hack, should be fixed in progress.py
			return

		print('\n Decrypting...\n')
		decryptor = Decryptor(password, target_path)
		decryptor.decryptFile(target_size)
		if rm:
			os.remove(target_path)
		print('\r' + 20*' ' + '\r [■■■■■■■■■■] 100%') # TODO: This is a hack, should be fixed in progress.py
		return

	# If directory
	# Get all file paths in the directory recursively
	ff = files(target_path, mode)
	if len(ff) == 0:
		raise Exception('\n Error: ' + str(target_path) + ' is empty\n')

	password = getPassword(mode)
		
	# Get total size of files in the directory
	total_size = calcTotalSize(ff)

	if mode == ENCRYPT_MODE:
		print('\n Encrypting...\n')
		(key, salt) = deriveKey(password, None)
		for f in ff:
			encryptor = Encryptor(key, salt, f)
			encryptor.encryptFile(total_size)
			if rm:
				os.remove(f)
		print('\r' + 20*' ' + '\r [■■■■■■■■■■] 100%') # TODO: This is a hack, should be fixed in progress.py
		return

	print('\n Decrypting...\n')
	for f in ff:
		decryptor = Decryptor(password, f)
		decryptor.decryptFile(total_size)
		if rm:
			os.remove(f)
	print('\r' + 20*' ' + '\r [■■■■■■■■■■] 100%') # TODO: This is a hack, should be fixed in progress.py

if __name__ == '__main__':
	try:
		start()
	except KeyboardInterrupt:
		exit()
	except Exception as err:
		print('\r' + str(err))
		exit(1)
