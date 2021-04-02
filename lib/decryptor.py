from pathlib import Path
from typing import Dict
from functools import partial

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.passwd import derive_key
from lib.progress import Progress
from lib.file_extension import replace_file_ext
from lib.constants import HEADER_SIZE

def decrypt(password: str, f_in_path: Path, buffer_size: int, progress: Progress) -> (Path, str):
	header = _read_header(f_in_path)
	key, _ = derive_key(password, header['salt'])
	decryptor = Cipher(
		algorithms.AES(key), 
		modes.CBC(header['iv']), 
		backend=default_backend()
	).decryptor()

	f_out_ext = _unpad_ext(decryptor.update(header['cipher_ext']))
	f_out_path = replace_file_ext(f_in_path, f_out_ext)
	
	with open(f_in_path, 'rb') as fd_in:
		fd_in.seek(48) # Skip the header
		with open(f_out_path, 'wb') as fd_out:
			for chunk in iter(partial(fd_in.read, buffer_size), b''):
				progress.update(len(chunk))
				chunk = decryptor.update(chunk)
				chunk = _unpad_bytes(chunk)
				fd_out.write(chunk)
				progress.print()
			fd_out.write(decryptor.finalize())
	
	return f_out_path, f_out_ext

def _unpad_bytes(bytes_in: bytes) -> bytes:
	unpadder = padding.PKCS7(128).unpadder()
	try:
		return unpadder.update(bytes_in) + unpadder.finalize()
	except ValueError:
		return bytes_in

def _unpad_ext(ext: bytes) -> str:
	# 16B: length(2B) + ext(?) + pad(?) + b'kpk'(3B). e.g. 03txtppppppppkpk
	if ext[13:16] != b'kpk':
		raise Exception('invalid password')

	ext_length = None
	try:
		ext_length = int(ext[:2])
	except ValueError:
		raise Exception('invalid password')

	return str(ext[2:2 + ext_length], 'utf-8')

def _read_header(f_in_path: Path) -> Dict[str, bytes]:
	header = b''
	with open(f_in_path, 'rb') as fd_in:
		header = fd_in.read(HEADER_SIZE)
	return {
		'iv': header[0:16],
		'salt': header[16:32],
		'cipher_ext': header[32:64]
	}
