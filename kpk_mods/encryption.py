from os import urandom, path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from kpk_mods.progress import showProgress, calcPercentage
from kpk_mods.file_exntension import getFileExt, replaceFileExt
from kpk_mods.constants import BUFFER_SIZE

def encryptFile(encryptor, f_in_path, total_size):
	f_out_path = replaceFileExt(f_in_path, 'kpk')

	with open(f_in_path, 'rb') as f_in:
		r_byte = f_in.read(BUFFER_SIZE)
		if len(r_byte) % 16 != 0:
			padder = padding.PKCS7(128).padder()
			r_byte = padder.update(r_byte) + padder.finalize()

		with open(f_out_path, 'ab') as f_out:
			while r_byte != b'':
				w_byte = encryptor.update(r_byte)
				f_out.write(w_byte)

				percentage = calcPercentage(len(r_byte), total_size)
				showProgress(percentage)

				r_byte = f_in.read(BUFFER_SIZE)
				if len(r_byte) % 16 != 0:
					padder = padding.PKCS7(128).padder()
					r_byte = padder.update(r_byte) + padder.finalize()
			f_out.write(encryptor.finalize())

def writeMeta(encryptor, f_in_path, iv, salt):
	f_in_ext = getFileExt(f_in_path)
	f_out_path = replaceFileExt(f_in_path, 'kpk')

	# Overwrite error
	if path.exists(f_out_path):
		exit(' Error: ' + f_out_path + ' already exists\n')

	ext = bytes(f_in_ext, 'utf-8')
	# strech extension to 16B
	if len(ext) < 16:
		ext = urandom(9 - len(ext)) + b'%kapak%' + ext
	c_ext = encryptor.update(ext)

	# Write iv, salt, encrypted extension to first 48B of the output file
	f_out = open(f_out_path, 'wb')
	f_out.write(iv)
	f_out.write(salt)
	f_out.write(c_ext)
	f_out.close()

	return encryptor

def aesEncryptor(key):
	iv = urandom(16) # Generate random iv per file
	cipher = Cipher(
		algorithms.AES(key), 
		modes.CBC(iv), 
		backend=default_backend()
	)
	return (cipher.encryptor(), iv)