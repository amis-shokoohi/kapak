from os import urandom
from typing import Tuple

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes) -> Tuple[bytes, bytes]:
	password = bytes(password, 'utf-8')
	if not salt:
		salt = urandom(16)
	# Requires 256MB of RAM
	kdf = Scrypt(
		salt=salt,
		length=32,
		n=2**16, # number of iterations
		r=32, # block size
		p=1, # number of threads
		backend=default_backend()
	)
	key = kdf.derive(password)
	return (key, salt)