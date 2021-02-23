from os import urandom, path
from pathlib import Path
from functools import partial
from typing import BinaryIO, Dict

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.file_extension import file_ext, replace_file_ext
from lib.pipeline import new_pipeline

def encrypt(key: bytes, salt: bytes, f_in_path: Path, buffer_size: int):
	ext = file_ext(f_in_path)
	if len(ext) > 11:
		raise Exception('unable to encrypt files with extension longer than 11B')
	
	iv = urandom(16)
	encryptor = Cipher(
		algorithms.AES(key), 
		modes.CBC(iv), 
		backend=default_backend()
	).encryptor()

	header = {
		'iv': iv,
		'salt': salt,
		'cipher_ext': encryptor.update(_pad_ext(bytes(ext, 'utf-8')))
	}
	f_out_path = replace_file_ext(f_in_path, 'kpk')
	pipeline = new_pipeline(buffer_size)
	
	with open(f_in_path, 'rb') as fd_in:
		with open(f_out_path, 'wb') as fd_out:
			_write_header(fd_out, header)
			pipeline(
				fd_in,
				_pad_bytes,
				encryptor.update,
				fd_out
			)
			fd_out.write(encryptor.finalize())

def _pad_bytes(bytes_in: bytes) -> bytes:
	if len(bytes_in) % 16 == 0:
		return bytes_in
	padder = padding.PKCS7(128).padder()
	return padder.update(bytes_in) + padder.finalize()

def _pad_ext(ext: bytes) -> bytes:
	# Streches extension to 16B
	ext_length = len(ext)
	pad = urandom(11 - ext_length)
	ext_length_in_bytes = bytes(str(ext_length), 'utf-8')
	if ext_length < 10:
		ext_length_in_bytes = b'0' + ext_length_in_bytes
	padded_ext = ext_length_in_bytes + ext + pad + b'kpk'
	return padded_ext

def _write_header(fd_out: BinaryIO, header: Dict[str, bytes]):
	# Writes iv, salt & encrypted extension to first 48B of the output file
	fd_out.write(header['iv'])
	fd_out.write(header['salt'])
	fd_out.write(header['cipher_ext'])
