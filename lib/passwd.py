from pathlib import Path
from getpass import getpass
from sys import stderr
from typing import Tuple


def get_password(confirm: bool) -> str:
	password = ''
	# Read the password from password.txt file
	f = Path('password.txt')
	if f.exists():
		with open(f, 'r') as passwd_file:
			password = passwd_file.read().rstrip()
		f.unlink()
		is_correct, err_msg = _check_password_length(len(password))
		if not is_correct:
			raise Exception(err_msg)
	else: # Prompt user to enter the password
		password = _ask_pass(confirm)
		is_correct, err_msg = _check_password_length(len(password))
		if not is_correct:
			stderr.write('\nERROR: ' + err_msg + '\n\n')

		while not is_correct:
			password = _ask_pass(confirm)
			is_correct, err_msg = _check_password_length(len(password))
			if not is_correct:
				stderr.write('\nERROR: ' + err_msg + '\n\n')

	return password


def _ask_pass(confirm: bool) -> str:
	p1 = getpass('Enter password: ')

	if confirm:
		p2 = getpass('Reenter password: ')
		if p2 != p1:
			stderr.write('\nERROR: passwords do not match\n\n')
			return _ask_pass(True)

	return p1


def _check_password_length(pass_len: int) -> Tuple[bool, str]:
	if pass_len < 3:
		return False, 'password should be at least 3 characters'
	elif pass_len > 1024:
		return False, 'password is too long'
	return True, ''
