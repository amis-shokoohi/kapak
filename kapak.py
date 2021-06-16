import sys
import argparse
from pathlib import Path

import lib.message
import lib.encrypt
import lib.decrypt
from lib.constants import BUFFER_SIZE

def main():
	argv = sys.argv
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
		parser = argparse.ArgumentParser(prog='kapak encrypt', add_help=False)
		parser.add_argument('-z', '--zip', action='store_true', dest='should_zip')
		parser.add_argument('-r', '--remove', action='store_true', dest='should_remove')
		parser.add_argument('-b', '--buffer-size', nargs='?', type=int, default=BUFFER_SIZE, dest='buffer_size')
		parser.add_argument('path', type=Path)
		args = parser.parse_args(args=argv[2:])
		lib.encrypt.execute(
			path=args.path, 
			buffer_size=args.buffer_size, 
			should_remove=args.should_remove, 
			should_zip=args.should_zip
		)
	elif argv[1] == 'decrypt':
		if len(argv) == 2 or argv[2] == '-h' or argv[2] == '--help':
			lib.message.print_help_decrypt()
			return
		parser = argparse.ArgumentParser(prog='kapak decrypt', add_help=False)
		parser.add_argument('-r', '--remove', action='store_true', dest='should_remove')
		parser.add_argument('-b', '--buffer-size', nargs='?', type=int, default=BUFFER_SIZE, dest='buffer_size')
		parser.add_argument('path', type=Path)
		args = parser.parse_args(args=argv[2:])
		lib.decrypt.execute(
			path=args.path, 
			buffer_size=args.buffer_size, 
			should_remove=args.should_remove
		)
	else:
		lib.message.print_help()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()
	except Exception as err:
		sys.stderr.write('\r' + 40*' ' + '\r\nERROR: ' + err.args[0] + '\n')
		sys.exit(1)
