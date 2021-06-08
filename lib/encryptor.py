from os import urandom, path
from pathlib import Path
from functools import partial

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.file_extension import file_ext, replace_file_ext
from lib.progress import Progress

def encrypt(f_in_path: Path, key: bytes, salt: bytes, buffer_size: int, progress: Progress):
	ext = file_ext(f_in_path)
	if len(ext) > 11: # 16B = 2B ext length + 11B ext + 0B padding + 3B b'kpk'
		raise Exception('unable to encrypt files with extension longer than 11 characters')
	
	iv = urandom(16)
	encryptor = Cipher(
		algorithms.AES(key), 
		modes.CBC(iv), 
		backend=default_backend()
	).encryptor()

	cipher_ext = encryptor.update(_pad_ext(bytes(ext, 'utf-8')))
	f_out_path = replace_file_ext(f_in_path, 'kpk')
	
	with open(f_in_path, 'rb') as fd_in:
		with open(f_out_path, 'wb') as fd_out:
			# Write header
			fd_out.write(iv + salt + cipher_ext)

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

def _pad_ext(ext: bytes) -> bytes:
	# Streches extension to 16B
	ext_length = len(ext)
	pad = bytes(''.zfill(11 - ext_length), 'utf-8')
	ext_length_in_bytes = bytes(str(ext_length), 'utf-8')
	if ext_length < 10:
		ext_length_in_bytes = b'0' + ext_length_in_bytes
	padded_ext = ext_length_in_bytes + ext + pad + b'kpk'
	return padded_ext
