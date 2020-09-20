from os import stat
from re import split
from math import ceil

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from kpk_mods.passwd import deriveKey
from kpk_mods.progress import showProgress, calcPercentage
from kpk_mods.file_exntension import replaceFileExt
from kpk_mods.constants import BUFFER_SIZE

class Decryptor():
	def __init__(self, password, f_in):
		meta = self.readMeta(f_in)
		(key, _) = deriveKey(password, meta['salt'])
		self.decryptor = self.aesDecryptor(key, meta['iv'])
		f_out_ext = self.decryptExt(meta['c_ext'])
		self.f_out = replaceFileExt(f_in, f_out_ext)
		self.f_in = f_in
		self.f_in_size = stat(f_in).st_size - 48

	def decryptFile(self, total_size):
		with open(self.f_in, 'rb') as f_in:
			f_in.read(48)
			r_byte = f_in.read(BUFFER_SIZE)

			with open(self.f_out, 'wb') as f_out:
				unpadder = padding.PKCS7(128).unpadder()
				if self.f_in_size < BUFFER_SIZE:
					w_byte = self.decryptor.update(r_byte)
					try:
						w_byte = unpadder.update(w_byte) + unpadder.finalize()
					except ValueError:
						pass
					f_out.write(w_byte)

					percentage = calcPercentage(self.f_in_size, total_size)
					showProgress(percentage)

					f_out.write(self.decryptor.finalize())
					return

				for i in range(1, ceil(self.f_in_size / BUFFER_SIZE) + 1):
					w_byte = self.decryptor.update(r_byte)
					if i == ceil(self.f_in_size / BUFFER_SIZE):
						try:
							w_byte = unpadder.update(w_byte) + unpadder.finalize()
						except ValueError:
							pass
					f_out.write(w_byte)

					percentage = calcPercentage(len(r_byte), total_size)
					showProgress(percentage)

					r_byte = f_in.read(BUFFER_SIZE)
				f_out.write(self.decryptor.finalize())

	def decryptExt(self, c_ext):
		ext = self.decryptor.update(c_ext)
		if len(split(b'%kapak%', ext)) < 2:
			raise Exception(' Error: Invalid password\n')
		f_out_ext = str(split(b'%kapak%', ext)[1], 'utf-8')
		return f_out_ext

	def readMeta(self, f_in_path):
		# Extract iv, salt, encrypted extension
		f_in = open(f_in_path, 'rb')
		iv = f_in.read(16)
		salt = f_in.read(16)
		c_ext = f_in.read(16)
		f_in.close()
		return {
			'iv': iv,
			'salt': salt,
			'c_ext': c_ext
		}

	def aesDecryptor(self, key, iv):
		cipher = Cipher(
			algorithms.AES(key), 
			modes.CBC(iv), 
			backend=default_backend()
		)
		return cipher.decryptor()