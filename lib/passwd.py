from pathlib import Path
from getpass import getpass
from sys import stderr

from lib.constants import DECRYPT_MODE

def get_password(mode: int) -> str:
	password = None
	# Read the password from password.txt file
	f = Path('password.txt')
	if f.exists():
		with open(f, 'r') as passwd_file:
			password = str(passwd_file.read())
		f.unlink()
	else: # Prompt user to enter the password
		password = _ask_pass(mode)
	
	while not _is_correct_pass_length(password):
		password = _ask_pass(mode)

	return password

def _ask_pass(mode: int) -> str:
	password1 = getpass('Enter password: ')

	if mode == DECRYPT_MODE:
		return password1
		
	password2 = getpass('Retype password: ')
	while password1 != password2:
		stderr.write('\nERROR: passwords do not match\n\n')
		password1 = getpass('Enter password: ')
		password2 = getpass('Retype password: ')
	return password2

def _is_correct_pass_length(password: str) -> bool:
	if len(password) < 3:
		stderr.write('\nERROR: password should be at least 3 characters\n\n')
		return False
	elif len(password) > 1024:
		stderr.write('\nERROR: password is to long\n\n')
		return False
	return True
