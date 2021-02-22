from sys import argv, exit, stderr

from libkapak.message import print_description, print_help, print_version
import libkapak.cli_encrypt
import libkapak.cli_decrypt

def main():
	if len(argv) == 1:
		print_description()
	elif argv[1] == '-h' or argv[1] == '--help':
		print_help()
	elif argv[1] == '-v' or argv[1] == '--version':
		print_version()
	elif argv[1] == 'encrypt':
		libkapak.cli_encrypt.execute(argv)
	elif argv[1] == 'decrypt':
		libkapak.cli_decrypt.execute(argv)
	else:
		print_help()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()
	except Exception as err:
		stderr.write('\r' + 40*' ' + '\r\nERROR: ' + err.args[0] + '\n')
		exit(1)
