from os import urandom
from pathlib import Path
from functools import partial

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.file_extension import file_ext, replace_file_ext
from lib.progress import Progress
from lib.constants import VERSION


def encrypt(f_in_path: Path, key: bytes, salt: bytes, buffer_size: int, progress: Progress):
	major_version = bytes(VERSION.split('.')[0][1:].zfill(4), 'utf-8') # 4B

	ext = file_ext(f_in_path)
	ext_length = bytes(str(len(ext)).zfill(4), 'utf-8')
	
	iv = urandom(16)
	encryptor = Cipher(
		algorithms.AES(key), 
		modes.CBC(iv), 
		backend=default_backend()
	).encryptor()

	cipher_ext = encryptor.update(_pad_bytes(bytes(ext, 'utf-8')))

	header = major_version + iv + salt + ext_length + cipher_ext
	header_length = bytes(str(len(header)).zfill(4), 'utf-8') # 4B
	
	f_out_path = replace_file_ext(f_in_path, 'kpk')
	with open(f_in_path, 'rb') as fd_in:
		with open(f_out_path, 'wb') as fd_out:
			# Write header
			fd_out.write(header_length + header)

			for chunk in iter(partial(fd_in.read, buffer_size), b''):
				progress.update(len(chunk))
				chunk = _pad_bytes(chunk)
				chunk = encryptor.update(chunk)
				fd_out.write(chunk)
				progress.print()
			fd_out.write(encryptor.finalize())


def _pad_bytes(bytes_in: bytes) -> bytes:
	if len(bytes_in) % 16 == 0:
		return bytes_in
	padder = padding.PKCS7(128).padder()
	return padder.update(bytes_in) + padder.finalize()
