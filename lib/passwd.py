from os import path, remove, urandom
from getpass import getpass

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

from lib.constants import DECRYPT_MODE

def _ask_pass(mode):
	password1 = getpass('Enter password: ')
	password2 = None

	if mode == DECRYPT_MODE:
		return password1
		
	password2 = getpass('Retype password: ')
	while password1 != password2:
		print('\nERROR: passwords do not match\n')
		password1 = getpass('Enter password: ')
		password2 = getpass('Retype password: ')
	return password2
	

def _is_correct_pass_length(password):
	if len(password) < 3:
		print('\nERROR: password should be at least 3 characters\n')
		return False
	elif len(password) > 1024:
		print('\nERROR: password is to long\n')
		return False
	return True

def get_password(mode):
	password = None
	# Read the password from password.txt file
	f = 'password.txt'
	if path.exists(f):
		passwd_file = open(f, 'r')
		password = passwd_file.read()
		passwd_file.close()
		remove(f)
	else: # Prompt user to enter the password
		password = _ask_pass(mode)
	
	while not _is_correct_pass_length(password):
		password = _ask_pass(mode)

	return password

# Needs at least 256MB of RAM
# Takes about a second to derive a key
def derive_key(password, salt):
	password = bytes(password, 'utf-8')
	if not salt:
		salt = urandom(16)
	kdf = Scrypt(
		salt=salt,
		length=32,
		n=2**16,
		r=32,
		p=1,
		backend=default_backend()
	)
	key = kdf.derive(password)
	return (key, salt)
