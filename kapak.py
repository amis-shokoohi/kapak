import os
import re
from sys import argv, exit
from pathlib import Path

from kpk_mods.args_parse import hasRemoveFlag, whichMode, getPath
from kpk_mods.passwd import getPassword, deriveKey
from kpk_mods.progress import getTotalSize
from kpk_mods.encryption import aesEncryptor, writeMeta, encryptFile
from kpk_mods.decryption import aesDecryptor, readMeta, decryptFile
from kpk_mods.message import printDescription, printHelp, printUsage
from kpk_mods.constants import ENCRYPT_MODE, DECRYPT_MODE

def getFilesList(dir_path, mode):
	fList = []

	if mode == ENCRYPT_MODE:
		allFiles = list(dir_path.glob('**/*'))
		for f in allFiles:
			if os.path.isdir(f):
				continue
			if str(f)[-3:] != 'kpk':
				fList.append(f)
	else:
		fList = list(dir_path.glob('**/*.kpk'))

	return fList

def start():
	# Usage message
	if len(argv) == 1:
		printDescription()
		exit()

	# Help message
	if argv[1] == '-h' or argv[1] == '--help':
		printHelp()
		exit()

	# Check for [-r] or [--remove] flag
	rm = hasRemoveFlag(argv)

	mode = whichMode(argv)
	if mode == None:
		printUsage()
		exit()
		
	p = Path(getPath(argv))
	if p == None:
		exit('\n Error: <path> variable NOT specified\n')
	elif not os.path.exists(p):
		exit('\n Error: Can NOT find ' + str(p) + '\n')

	if os.path.isdir(p):
		# Get all file paths in the directory recursively
		fList = getFilesList(p, mode)
		if len(fList) < 1:
			exit('\n Error: ' + str(p) + ' is empty\n')

		password = getPassword(mode)		
			
		# Get total size of files in the directory
		total_size = getTotalSize(fList)

		if mode == ENCRYPT_MODE:
			print('\n # Encrypting...\n')
			(key, salt) = deriveKey(password, None)
			for f in fList:
				(encryptor, iv) = aesEncryptor(key)
				encryptor = writeMeta(encryptor, f, iv, salt)
				encryptFile(encryptor, f, total_size)

				if rm:
					os.remove(f)
		else:
			print('\n # Decrypting...\n')
			for f in fList:
				(decryptor, f_out_ext) = readMeta(f, password)
				decryptFile(decryptor, f, total_size, f_out_ext)

				if rm:
					os.remove(f)
	elif os.path.isfile(p):
		if mode == ENCRYPT_MODE and str(p)[-3:] == 'kpk':
			exit('\n Error: Can NOT encrypt ' + str(p) + '\n')

		password = getPassword(mode)
		
		p_size = os.stat(p).st_size

		if mode == ENCRYPT_MODE:
			(key, salt) = deriveKey(password, None)
			print('\n # Encrypting...\n')

			(encryptor, iv) = aesEncryptor(key)
			encryptor = writeMeta(encryptor, p, iv, salt)
			encryptFile(encryptor, p, p_size)

			if rm:
				os.remove(p)
		else:
			print('\n # Decrypting...\n')

			(decryptor, f_out_ext) = readMeta(p, password)
			decryptFile(decryptor, p, p_size, f_out_ext)

			if rm:
				os.remove(p)

if __name__ == '__main__':
	try:
		start()
	except KeyboardInterrupt:
		exit()
