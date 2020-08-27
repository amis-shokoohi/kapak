from os import stat
from sys import exit
from re import split
from math import ceil

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from kpk_mods.passwd import deriveKey
from kpk_mods.progress import showProgress, calcPercentage
from kpk_mods.file_exntension import getFileExt, replaceFileExt
from kpk_mods.constants import BUFFER_SIZE

def decryptFile(decryptor, f_in_path, total_size, f_out_ext):
	f_out_path = replaceFileExt(f_in_path, f_out_ext)

	f_in_size = stat(f_in_path).st_size - 48
	with open(f_in_path, 'rb') as f_in:
		f_in.read(48)
		r_byte = f_in.read(BUFFER_SIZE)

		with open(f_out_path, 'wb') as f_out:
			unpadder = padding.PKCS7(128).unpadder()
			if f_in_size < BUFFER_SIZE:
				w_byte = decryptor.update(r_byte)
				try:
					w_byte = unpadder.update(w_byte) + unpadder.finalize()
				except ValueError:
					pass
				f_out.write(w_byte)

				percentage = calcPercentage(f_in_size, total_size)
				showProgress(percentage)
			else:
				for i in range(1, ceil(f_in_size / BUFFER_SIZE) + 1):
					w_byte = decryptor.update(r_byte)
					if i == ceil(f_in_size / BUFFER_SIZE):
						try:
							w_byte = unpadder.update(w_byte) + unpadder.finalize()
						except ValueError:
							pass
					f_out.write(w_byte)

					percentage = calcPercentage(len(r_byte), total_size)
					showProgress(percentage)

					r_byte = f_in.read(BUFFER_SIZE)

			f_out.write(decryptor.finalize())

def readMeta(f_in_path, password):
	f_in_ext = getFileExt(f_in_path)
	if f_in_ext != 'kpk':
		exit(' Error: Can NOT decrypt ' + str(f_in_path) + '\n')

	# Extract iv, salt, encrypted extension
	f_in = open(f_in_path, 'rb')
	iv = f_in.read(16)
	salt = f_in.read(16)
	c_ext = f_in.read(16)
	f_in.close()

	# Derive the key
	(key, _) = deriveKey(password, salt)

	decryptor = aesDecryptor(key, iv)

	ext = decryptor.update(c_ext)

	if len(split(b'%kapak%', ext)) < 2:
		exit(' Error: Invalid password\n')

	f_out_ext = str(split(b'%kapak%', ext)[1], 'utf-8')

	return (decryptor, f_out_ext)

def aesDecryptor(key, iv):
	cipher = Cipher(
		algorithms.AES(key), 
		modes.CBC(iv), 
		backend=default_backend()
	)
	return cipher.decryptor()