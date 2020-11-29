import os
from sys import argv, exit
from pathlib import Path

from kpk_mods.arg_parse import hasRemoveFlag, whichMode, getPath
from kpk_mods.passwd import getPassword, deriveKey
from kpk_mods.decryption import Decryptor
from kpk_mods.encryption import Encryptor
from kpk_mods.message import printDescription, printHelp, printUsage
from kpk_mods.dir import files, calcTotalSize
from kpk_mods.constants import ENCRYPT_MODE
from kpk_mods.file_exntension import validateFileByExt

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
			return

		print('\n Decrypting...\n')
		decryptor = Decryptor(password, target_path)
		decryptor.decryptFile(target_size)
		if rm:
			os.remove(target_path)
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
		return

	print('\n Decrypting...\n')
	for f in ff:
		decryptor = Decryptor(password, f)
		decryptor.decryptFile(total_size)
		if rm:
			os.remove(f)

if __name__ == '__main__':
	try:
		start()
	except KeyboardInterrupt:
		exit()
	except Exception as err:
		print('\r' + str(err))
		exit(1)
