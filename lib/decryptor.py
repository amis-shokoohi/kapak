from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.passwd import derive_key
from lib.progress import Progress
from lib.file_exntension import replace_file_ext
from lib.pipeline import pipeline

class FileDecryptor():
	def __init__(self, password: str, f_in_path: Path):
		self.__f_in_path = f_in_path
		self.__progress = Progress.get_instance()

		header = self.__read_header()
		key, _ = derive_key(password, header['salt'])
		self.__decryptor = self.__aes_decryptor(key, header['iv'])

		self.__f_out_ext = self.__decrypt_ext(header['cipher_ext'])
		self.__f_out_path = replace_file_ext(f_in_path, self.__f_out_ext)

	def get_file_name(self) -> Path:
		return self.__f_out_path

	def get_file_ext(self) -> str:
		return self.__f_out_ext

	def decrypt(self):
		with open(self.__f_in_path, 'rb') as fd_in:
			fd_in.seek(48) # Skip the header
			with open(self.__f_out_path, 'wb') as fd_out:
				pipeline(fd_in, fd_out, self.__update)
				fd_out.write(self.__decryptor.finalize())

	def __update(self, in_bytes: bytes) -> bytes:
		out_bytes = self.__decryptor.update(in_bytes)
		try:
			unpadder = padding.PKCS7(128).unpadder()
			out_bytes = unpadder.update(out_bytes) + unpadder.finalize()
		except ValueError:
			pass
		self.__progress.calc_percentage(len(in_bytes))
		self.__progress.print_percentage()
		return out_bytes

	def __decrypt_ext(self, cipher_ext: bytes) -> str:
		# 16B: length(2B) + ext(?) + pad(?) + b'kpk'(3B). e.g. 03txtppppppppkpk
		ext = self.__decryptor.update(cipher_ext)

		if ext[13:16] != b'kpk':
			raise Exception('invalid password')

		ext_length = None
		try:
			ext_length = int(ext[:2])
		except ValueError:
			raise Exception('invalid password')

		return str(ext[2:2 + ext_length], 'utf-8')

	def __read_header(self) -> dict:
		header = {
			'iv': None,
			'salt': None,
			'cipher_ext': None
		}
		with open(self.__f_in_path, 'rb') as fd_in:
			header['iv'] = fd_in.read(16)
			header['salt'] = fd_in.read(16)
			header['cipher_ext'] = fd_in.read(16)
		self.__progress.calc_percentage(48)
		self.__progress.print_percentage()	
		return header

	def __aes_decryptor(self, key: bytes, iv: bytes):
		cipher = Cipher(
			algorithms.AES(key), 
			modes.CBC(iv), 
			backend=default_backend()
		)
		return cipher.decryptor()