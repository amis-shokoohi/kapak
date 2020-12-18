from os import path, remove, urandom
from getpass import getpass

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

from lib.constants import ENCRYPT_MODE

def askPass(mode):
	password1 = getpass(' Enter password: ')
	password2 = None
	if mode == ENCRYPT_MODE:
		password2 = getpass(' Retype password: ')
		while password1 != password2:
			print('\n Error: Passwords do NOT match\n')
			password1 = getpass(' Enter password: ')
			password2 = getpass(' Retype password: ')
	return password1

def isCorrectPassLength(password):
	if len(password) < 3:
		print('\n Error: Password should be at least 3 characters\n')
		return False
	elif len(password) > 1024:
		print('\n Error: Password is to large\n')
		return False
	return True

def getPassword(mode):
	password = None
	# Read the password from password.txt file
	f = 'password.txt'
	if path.exists(f):
		pFile = open(f, 'r')
		password = pFile.read()
		pFile.close()
		remove(f)
	# Prompt user for the password
	else:
		password = askPass(mode)
	
	while not isCorrectPassLength(password):
		password = askPass(mode)

	return password

# Needs at least 256MB of RAM
# Takes about a second to derive key
def deriveKey(password, salt):
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
