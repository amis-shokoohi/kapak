from os import urandom, path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.progress import Progress
from lib.file_exntension import file_ext, replace_file_ext
from lib.pipeline import pipeline

class FileEncryptor():
	def __init__(self, key, salt, f_in_path):
		self.__f_in_path = f_in_path
		self.__f_out_path = replace_file_ext(f_in_path, 'kpk')
		self.__progress = Progress.get_instance()

		iv = urandom(16) # Generate random iv per file
		self.__encryptor = self.__aes_encryptor(key, iv)
		self.__header = {
			'iv': iv,
			'salt': salt,
			'cipher_ext': None
		}

	def encrypt(self):
		ext = file_ext(self.__f_in_path)
		self.__header['cipher_ext'] = self.__encrypt_ext(ext)
		with open(self.__f_in_path, 'rb') as fd_in:
			with open(self.__f_out_path, 'wb') as fd_out:
				self.__write_header(fd_out)
				pipeline(fd_in, fd_out, self.__update)
				fd_out.write(self.__encryptor.finalize())

	def __update(self, in_bytes):
		if len(in_bytes) % 16 != 0:
			padder = padding.PKCS7(128).padder()
			in_bytes = padder.update(in_bytes) + padder.finalize()
		out_bytes = self.__encryptor.update(in_bytes)
		self.__progress.calc_percentage(len(in_bytes))
		self.__progress.print_percentage()
		return out_bytes

	def __encrypt_ext(self, ext):
		ext = bytes(ext, 'utf-8')
		ext_length = len(ext)
		if ext_length > 11:
			raise Exception('unable to encrypt files with extension longer than 11B')

		# Strech extension to 16B
		pad = urandom(11 - ext_length)
		ext_length_in_bytes = bytes(str(ext_length), 'utf-8')
		if ext_length < 9:
			ext_length_in_bytes = b'0' + ext_length_in_bytes
		ext = ext_length_in_bytes + ext + pad + b'kpk'
		return self.__encryptor.update(ext)

	def __write_header(self, fd_out):
		# Writes iv, salt & encrypted extension to first 48B of the output file
		fd_out.write(self.__header['iv'])
		fd_out.write(self.__header['salt'])
		fd_out.write(self.__header['cipher_ext'])

	def __aes_encryptor(self, key, iv):
		cipher = Cipher(
			algorithms.AES(key), 
			modes.CBC(iv), 
			backend=default_backend()
		)
		return cipher.encryptor()