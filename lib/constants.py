BUFFER_SIZE = 64 * 1024 * 1024 # 64MB
TEMP_ZIP_EXT = 'kpktempzip'

ENCRYPT_MODE = 1
DECRYPT_MODE = 2

_VERSION = 'v2.2.0'
_BY = 'Amis Shokoohi'

LOGO = '\n\
    ▄ •▄  ▄▄▄·  ▄▄▄· ▄▄▄· ▄ •▄ \n\
    █▌▄▌▪▐█ ▀█ ▐█ ▄█▐█ ▀█ █▌▄▌▪\n\
    ▐▀▀▄·▄█▀▀█  ██▀·▄█▀▀█ ▐▀▀▄·\n\
    ▐█.█▌▐█ ▪▐▌▐█▪·•▐█ ▪▐▌▐█.█▌    {version}\n\
    ·▀  ▀ ▀  ▀ .▀    ▀  ▀ ·▀  ▀    by {by}\n\
'.format(version=_VERSION, by=_BY)

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
