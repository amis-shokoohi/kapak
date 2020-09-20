from os import urandom, path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from kpk_mods.progress import showProgress, calcPercentage
from kpk_mods.file_exntension import fileExt, replaceFileExt
from kpk_mods.constants import BUFFER_SIZE

class Encryptor():
	def __init__(self, key, salt, f_in):
		iv = urandom(16) # Generate random iv per file
		self.encryptor = self.aesEncryptor(key, iv)
		ext = fileExt(f_in)

		meta = { 'iv': None, 'salt': None, 'c_ext': None }
		meta['salt'] = salt
		meta['iv'] = iv
		meta['c_ext'] = self.encryptExt(ext)

		self.f_out = replaceFileExt(f_in, 'kpk')
		self.f_in = f_in

		# Overwrite error
		if path.exists(self.f_out):
			raise Exception(' Error: ' + self.f_out + ' already exists\n')

		self.writeMeta(self.f_out, meta)

	def encryptFile(self, total_size):
		with open(self.f_in, 'rb') as f_in:
			r_byte = f_in.read(BUFFER_SIZE)
			if len(r_byte) % 16 != 0:
				padder = padding.PKCS7(128).padder()
				r_byte = padder.update(r_byte) + padder.finalize()

			with open(self.f_out, 'ab') as f_out:
				while r_byte != b'':
					w_byte = self.encryptor.update(r_byte)
					f_out.write(w_byte)

					percentage = calcPercentage(len(r_byte), total_size)
					showProgress(percentage)

					r_byte = f_in.read(BUFFER_SIZE)
					if len(r_byte) % 16 != 0:
						padder = padding.PKCS7(128).padder()
						r_byte = padder.update(r_byte) + padder.finalize()
				f_out.write(self.encryptor.finalize())

	def encryptExt(self, ext):
		ext = bytes(ext, 'utf-8')
		if len(ext) > 11:
			raise Exception(' Error: Unable to encrypt files with extension longer than 11B\n')
		# Strech extension to 16B
		ext = urandom(11 - len(ext)) + b'%kpk%' + ext
		return self.encryptor.update(ext)

	def writeMeta(self, f_out_path, meta):
		# Write iv, salt, encrypted extension to first 48B of the output file
		f_out = open(f_out_path, 'wb')
		f_out.write(meta['iv'])
		f_out.write(meta['salt'])
		f_out.write(meta['c_ext'])
		f_out.close()

	def aesEncryptor(self, key, iv):
		cipher = Cipher(
			algorithms.AES(key), 
			modes.CBC(iv), 
			backend=default_backend()
		)
		return cipher.encryptor()