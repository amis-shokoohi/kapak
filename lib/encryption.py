from os import urandom, path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.progress import Progress
from lib.file_exntension import file_ext, replace_file_ext
from lib.constants import BUFFER_SIZE

class FileEncryptor():
	def __init__(self, key, salt, f_in_path):
		self.__f_in_path = f_in_path

		iv = urandom(16) # Generate random iv per file
		self.__encryptor = self.__aes_encryptor(key, iv)

		meta = { 'iv': None, 'salt': None, 'c_ext': None }
		meta['salt'] = salt
		meta['iv'] = iv
		ext = file_ext(f_in_path)
		meta['c_ext'] = self.__encrypt_ext(ext)

		self.__f_out_path = replace_file_ext(f_in_path, 'kpk')
		if path.exists(self.__f_out_path): # Overwrite error
			raise Exception(self.__f_out_path + ' already exists')

		self.__fd_out = open(self.__f_out_path, 'wb')
		self.__write_meta(meta)

		self.__progress = Progress.get_instance()

	def encrypt(self):
		with open(self.__f_in_path, 'rb') as f_in:
			r_byte = f_in.read(BUFFER_SIZE)
			if len(r_byte) % 16 != 0:
				padder = padding.PKCS7(128).padder()
				r_byte = padder.update(r_byte) + padder.finalize()

			with self.__fd_out as f_out:
				while r_byte != b'':
					w_byte = self.__encryptor.update(r_byte)
					f_out.write(w_byte)

					self.__progress.calc_percentage(len(r_byte))
					self.__progress.print_percentage()

					r_byte = f_in.read(BUFFER_SIZE)
					if len(r_byte) % 16 != 0:
						padder = padding.PKCS7(128).padder()
						r_byte = padder.update(r_byte) + padder.finalize()
				f_out.write(self.__encryptor.finalize())

	def __encrypt_ext(self, ext):
		ext = bytes(ext, 'utf-8')
		ext_length = len(ext)
		if ext_length > 11:
			raise Exception('unable to encrypt files with extension longer than 11B')

		# Strech extension to 16B
		pad = urandom(11 - ext_length)
		if ext_length < 9:
			ext_length = bytes('0' + str(ext_length), 'utf-8')
		else:
			ext_length = bytes(str(ext_length), 'utf-8')
		ext = ext_length + ext + pad + b'kpk'
		
		return self.__encryptor.update(ext)

	def __write_meta(self, meta):
		# Write iv, salt, encrypted extension to first 48B of the output file
		self.__fd_out.write(meta['iv'])
		self.__fd_out.write(meta['salt'])
		self.__fd_out.write(meta['c_ext'])

	def __aes_encryptor(self, key, iv):
		cipher = Cipher(
			algorithms.AES(key), 
			modes.CBC(iv), 
			backend=default_backend()
		)
		return cipher.encryptor()