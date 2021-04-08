from sys import argv, exit, stderr
import argparse
from pathlib import Path

import lib.message
import lib.cli_encrypt
import lib.cli_decrypt
from lib.constants import BUFFER_SIZE

def main():
	if len(argv) == 1:
		lib.message.print_description()
	elif argv[1] == '-h' or argv[1] == '--help':
		lib.message.print_help()
	elif argv[1] == '-v' or argv[1] == '--version':
		lib.message.print_version()
	elif argv[1] == 'encrypt':
		if len(argv) == 2 or argv[2] == '-h' or argv[2] == '--help':
			lib.message.print_help_encrypt()
			return
		parser = argparse.ArgumentParser(prog="kapak encrypt", add_help=False)
		parser.add_argument('-z', '--zip', action='store_true', dest='should_zip')
		parser.add_argument('-r', '--remove', action='store_true', dest='should_remove')
		parser.add_argument('-b', '--buffer-size', nargs='?', type=int, default=BUFFER_SIZE, dest='buffer_size')
		parser.add_argument('path', type=Path)
		args = parser.parse_args(args=argv[2:])
		lib.cli_encrypt.execute(args)
	elif argv[1] == 'decrypt':
		if len(argv) == 2 or argv[2] == '-h' or argv[2] == '--help':
			lib.message.print_help_decrypt()
			return
		parser = argparse.ArgumentParser(prog='kapak decrypt', add_help=False)
		parser.add_argument('-r', '--remove', action='store_true', dest='should_remove')
		parser.add_argument('-b', '--buffer-size', nargs='?', type=int, default=BUFFER_SIZE, dest='buffer_size')
		parser.add_argument('path', type=Path)
		args = parser.parse_args(args=argv[2:])
		lib.cli_decrypt.execute(args)
	else:
		lib.message.print_help()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()
	except Exception as err:
		stderr.write('\r' + 40*' ' + '\r\nERROR: ' + err.args[0] + '\n')
		exit(1)
