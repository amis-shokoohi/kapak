from pathlib import Path
from typing import Dict, Tuple, Union
from functools import partial

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from lib.key import derive_key
from lib.progress import Progress
from lib.file_extension import replace_file_ext
from lib.constants import VERSION


def decrypt(f_in_path: Path, password: str, buffer_size: int, progress: Progress) -> Tuple[Path, str]:
	header = _read_header(f_in_path)
	header_length = header['header_length']
	progress.update(header_length)

	# Check version
	major_version = int(VERSION.split('.')[0][1:])
	if header['major_version'] != major_version:
		raise Exception('need Kapak version ' + str(major_version) + ' to decrypt ' + str(f_in_path))

	key, _ = derive_key(password, header['salt'])
	decryptor = Cipher(
		algorithms.AES(key), 
		modes.CBC(header['iv']), 
		backend=default_backend()
	).decryptor()

	# Decrypt file extension
	try:
		f_out_ext = str(_unpad_bytes(decryptor.update(header['cipher_ext'])), 'utf-8')
		if len(f_out_ext) != header['ext_length']:
			raise Exception('wrong password')
	except UnicodeDecodeError:
			raise Exception('wrong password')

	f_out_path = replace_file_ext(f_in_path, f_out_ext)
	with open(f_in_path, 'rb') as fd_in:
		fd_in.seek(header_length) # Skip the header
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


def _read_header(f_in_path: Path) -> Dict[str, Union[bytes, int]]:
	header = b''
	header_length = 0
	with open(f_in_path, 'rb') as f:
		try:
			header_length = int(f.read(4))
		except ValueError:
			raise Exception('need older versions of Kapak to decrypt ' + str(f_in_path))
		header = f.read(header_length)
	return {
		'header_length': 4 + header_length,
		'major_version': int(header[0:4]),
		'iv': header[4:20],
		'salt': header[20:36],
		'ext_length': int(header[36:40]),
		'cipher_ext': header[40:]
	}
