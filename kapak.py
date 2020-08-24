import os
import re
from sys import argv, exit
from pathlib import Path

from kpk_mods.passwd import getPassword, deriveKey
from kpk_mods.progress import getTotalSize, showProgressComplete
from kpk_mods.encryption import aesEncryptor, writeMeta, encryptFile
from kpk_mods.decryption import aesDecryptor, readMeta, decryptFile
from kpk_mods.message import printDescription, printHelp, printUsage
from kpk_mods.constants import ENCRYPT_MODE, DECRYPT_MODE

def hasRemoveFlag(argv):
	rm_flag = False
	flag_count = 0
	if len(argv) == 4:
		for v in argv[1:]:
			if v == '-r' or v == '--remove':
				rm_flag = True
				flag_count += 1

		if flag_count < 1 or flag_count > 2:
			exit('\n Error: Incorrect remove flag\n')

	return rm_flag

def whichMode(argv):
	mode_flag = None
	flag_count = 0
	if len(argv) == 3 or len(argv) == 4:
		for v in argv[1:]:
			if v == '-e' or v == '--encrypt':
				mode_flag = ENCRYPT_MODE
				flag_count += 1
			elif v == '-d' or v == '--decrypt':
				mode_flag = DECRYPT_MODE
				flag_count += 1

		if flag_count > 1:
			mode_flag = None

	return mode_flag

def getPath(agrv):
	if len(argv) == 3 or len(argv) == 4:
		for v in argv[1:]:
			if v[0:1] != '-':
				return v
	return None

def getFilesList(dir_path, mode):
	fList = []

	if mode == ENCRYPT_MODE:
		allFiles = list(dir_path.glob('**/*'))
		for f in allFiles:
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

		if mode == ENCRYPT_MODE:
			print('\n # Encrypting...\n')
		else:
			print('\n # Decrypting...\n')
			
		# Get total size of files in the directory
		total_size = getTotalSize(fList)

		if mode == ENCRYPT_MODE:
			(key, salt) = deriveKey(password, None)
			for f in fList:
				if os.path.isdir(f):
					continue
				
				(encryptor, iv) = aesEncryptor(key)
				encryptor = writeMeta(encryptor, f, iv, salt)
				encryptFile(encryptor, f, total_size)

				if rm:
					os.remove(f)
		else:
			for f in fList:
				if os.path.isdir(f):
					continue

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

	showProgressComplete()

if __name__ == '__main__':
	try:
		start()
	except KeyboardInterrupt:
		exit()
