from lib.constants import VERSION, BUFFER_SIZE

def print_description():
	print(DESCRIPTION)

def print_version():
	v = '\nkapak {version}\n'.format(version=VERSION)
	print(v)

def print_help():
	print(USAGE)

def print_help_encrypt():
	print(USAGE_ENCRYPT)

def print_help_decrypt():
	print(USAGE_DECRYPT)

DESCRIPTION = '''
    ▄ •▄  ▄▄▄·  ▄▄▄· ▄▄▄· ▄ •▄ 
    █▌▄▌▪▐█ ▀█ ▐█ ▄█▐█ ▀█ █▌▄▌▪
    ▐▀▀▄·▄█▀▀█  ██▀·▄█▀▀█ ▐▀▀▄·
    ▐█.█▌▐█ ▪▐▌▐█▪·•▐█ ▪▐▌▐█.█▌    {version}
    ·▀  ▀ ▀  ▀ .▀    ▀  ▀ ·▀  ▀

Description: A simple-to-use file encryption script
Link:        https://github.com/amis-shokoohi/kapak
Help:        kapak [ -h | --help ]
'''.format(version=VERSION)

USAGE = '''
usage: kapak [global options] <command> [command options] <path>

global options:
  -h, --help     Prints help message
  -v, --version  Prints version

commands:
  e, encrypt  Encrypts the specified file/directory
  d, decrypt  Decrypts the specified file/directory
'''

USAGE_ENCRYPT = '''
usage: kapak [encrypt | e] [options] <path>

options:
  -h, --help         Prints help message
  -r, --remove       Removes the target file/directory
  -z, --zip          Zips the directory before encryption
  -b, --buffer-size  Buffer size in megabytes (default: {buffer_size})
'''.format(buffer_size=BUFFER_SIZE)

USAGE_DECRYPT = '''
usage: kapak [decrypt | d] [options] <path>

options:
  -h, --help         Prints help message
  -r, --remove       Removes the target file/directory
  -b, --buffer-size  Buffer size in megabytes (default: {buffer_size})
'''.format(buffer_size=BUFFER_SIZE)