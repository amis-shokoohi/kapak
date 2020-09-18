import os
from sys import argv, exit
from pathlib import Path

from kpk_mods.arg_parse import hasRemoveFlag, whichMode, getPath
from kpk_mods.passwd import getPassword, deriveKey
from kpk_mods.encryption import aesEncryptor, writeMeta, encryptFile
from kpk_mods.decryption import readMeta, decryptFile
from kpk_mods.message import printDescription, printHelp, printUsage
from kpk_mods.dir import getFilesList, getTotalSize
from kpk_mods.constants import ENCRYPT_MODE

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
		if mode == ENCRYPT_MODE and str(target_path)[-3:] == 'kpk':
			raise Exception('\n Error: Can NOT encrypt ' + str(target_path) + '\n')

		password = getPassword(mode)
		
		target_size = os.stat(target_path).st_size

		if mode == ENCRYPT_MODE:
			print('\n # Encrypting...\n')
			(key, salt) = deriveKey(password, None)
			(encryptor, iv) = aesEncryptor(key)
			encryptor = writeMeta(encryptor, target_path, iv, salt)
			encryptFile(encryptor, target_path, target_size)
			if rm:
				os.remove(target_path)
			return

		print('\n # Decrypting...\n')
		(decryptor, f_out_ext) = readMeta(target_path, password)
		decryptFile(decryptor, target_path, target_size, f_out_ext)
		if rm:
			os.remove(target_path)
		return

	# If directory
	# Get all file paths in the directory recursively
	files = getFiles(target_path, mode)
	if len(files) == 0:
		raise Exception('\n Error: ' + str(target_path) + ' is empty\n')

	password = getPassword(mode)		
		
	# Get total size of files in the directory
	total_size = getTotalSize(files)

	if mode == ENCRYPT_MODE:
		print('\n # Encrypting...\n')
		(key, salt) = deriveKey(password, None)
		for f in files:
			(encryptor, iv) = aesEncryptor(key)
			encryptor = writeMeta(encryptor, f, iv, salt)
			encryptFile(encryptor, f, total_size)
			if rm:
				os.remove(f)
			return

	print('\n # Decrypting...\n')
	for f in files:
		(decryptor, f_out_ext) = readMeta(f, password)
		decryptFile(decryptor, f, total_size, f_out_ext)
		if rm:
			os.remove(f)

if __name__ == '__main__':
	try:
		start()
	except KeyboardInterrupt:
		exit()
	except Exception as err:
		exit(err)
