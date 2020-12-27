from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.passwd import derive_key
from lib.progress import Progress
from lib.file_exntension import replace_file_ext
from lib.constants import BUFFER_SIZE

class FileDecryptor():
	def __init__(self, password, f_in_path):
		self.__progress = Progress.get_instance()
		self.__fd_in = open(f_in_path, 'rb')

		meta = self.__read_meta()
		key, _ = derive_key(password, meta['salt'])
		self.__decryptor = self.__aes_decryptor(key, meta['iv'])

		self.__f_out_ext = self.__decrypt_ext(meta['c_ext'])
		self.__f_out_path = replace_file_ext(f_in_path, self.__f_out_ext)

	def get_decrypted_file_name(self):
		return self.__f_out_path

	def get_decrypted_file_ext(self):
		return self.__f_out_ext

	def decrypt(self):
		with self.__fd_in as f_in:
			r_byte = f_in.read(BUFFER_SIZE)
			with open(self.__f_out_path, 'wb') as f_out:
				unpadder = padding.PKCS7(128).unpadder()
				while r_byte != b'':
					w_byte = self.__decryptor.update(r_byte)
					try:
						w_byte = unpadder.update(w_byte) + unpadder.finalize()
					except ValueError:
						pass
					f_out.write(w_byte)

					self.__progress.calc_percentage(len(r_byte))
					self.__progress.print_percentage()

					r_byte = f_in.read(BUFFER_SIZE)
				f_out.write(self.__decryptor.finalize())

	def __decrypt_ext(self, c_ext):
		# 16B: length(2B) + ext(?) + pad(?) + b'kpk'(3B). e.g. 03txtppppppppkpk
		ext = self.__decryptor.update(c_ext)

		if ext[13:16] != b'kpk':
			raise Exception('invalid password')

		ext_length = None
		try:
			ext_length = int(ext[:2])
		except ValueError:
			raise Exception('invalid password')

		return str(ext[2:2 + ext_length], 'utf-8')

	def __read_meta(self):
		# Extract iv, salt, encrypted extension
		iv = self.__fd_in.read(16)
		salt = self.__fd_in.read(16)
		c_ext = self.__fd_in.read(16)

		self.__progress.calc_percentage(48)
		self.__progress.print_percentage()
		
		return {
			'iv': iv,
			'salt': salt,
			'c_ext': c_ext
		}

	def __aes_decryptor(self, key, iv):
		cipher = Cipher(
			algorithms.AES(key), 
			modes.CBC(iv), 
			backend=default_backend()
		)
		return cipher.decryptor()