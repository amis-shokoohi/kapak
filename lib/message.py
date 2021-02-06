def print_description():
	print(LOGO)
	print(DESCRIPTION)

def print_version():
	print(VERSION)

def print_help():
	print(USAGE)

def print_help_encrypt():
	print(USAGE_ENCRYPT)

def print_help_decrypt():
	print(USAGE_DECRYPT)

_VERSION = 'v3.0.1'

LOGO = '\n\
    ▄ •▄  ▄▄▄·  ▄▄▄· ▄▄▄· ▄ •▄ \n\
    █▌▄▌▪▐█ ▀█ ▐█ ▄█▐█ ▀█ █▌▄▌▪\n\
    ▐▀▀▄·▄█▀▀█  ██▀·▄█▀▀█ ▐▀▀▄·\n\
    ▐█.█▌▐█ ▪▐▌▐█▪·•▐█ ▪▐▌▐█.█▌    {version}\n\
    ·▀  ▀ ▀  ▀ .▀    ▀  ▀ ·▀  ▀\n\
'.format(version=_VERSION)

VERSION = '\nkapak {version}\n'.format(version=_VERSION)

DESCRIPTION = '\
Description: A simple-to-use file encryption script which\n\
             uses AES symmetric encryption methods\n\
Link:        https://github.com/amis-shokoohi/kapak\n\n\
Help:        kapak [ -h | --help ]\n\
'

USAGE = '\n\
Usage: kapak [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS] PATH\n\n\
Global Options:\n\
  -h, --help     Prints help message\n\
  -v, --version  Prints version\n\n\
Commands:\n\
  encrypt  Encrypts the specified file/directory\n\
  decrypt  Decrypts the specified file/directory\n\
'

USAGE_ENCRYPT = '\n\
Usage: kapak encrypt [OPTIONS] PATH\n\n\
Options:\n\
  -h, --help    Prints help message\n\
  -r, --remove  Removes the target file/directory\n\
  -z, --zip     Zips the directory before encryption\n\
'

USAGE_DECRYPT = '\n\
Usage: kapak decrypt [OPTIONS] PATH\n\n\
Options:\n\
  -h, --help    Prints help message\n\
  -r, --remove  Removes the target file/directory\n\
'