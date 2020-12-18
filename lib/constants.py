BUFFER_SIZE = 64 * 1024 * 1024 # 64MB

ENCRYPT_MODE = 1
DECRYPT_MODE = 2

_VERSION = 'v2.1.0'
_BY = 'Amis Shokoohi'

TITLE =  "\n\t▄ •▄  ▄▄▄·  ▄▄▄· ▄▄▄· ▄ •▄ "
TITLE += "\n\t█▌▄▌▪▐█ ▀█ ▐█ ▄█▐█ ▀█ █▌▄▌▪"
TITLE += "\n\t▐▀▀▄·▄█▀▀█  ██▀·▄█▀▀█ ▐▀▀▄·"
TITLE += "\n\t▐█.█▌▐█ ▪▐▌▐█▪·•▐█ ▪▐▌▐█.█▌" + "\t" + _VERSION
TITLE += "\n\t·▀  ▀ ▀  ▀ .▀    ▀  ▀ ·▀  ▀" + "\tby " + _BY
TITLE += "\n"

DESCRIPTION =    ' Description: \tA simple-to-use file encryption script which'
DESCRIPTION += '\n \t\tuses AES symmetric encryption methods'
DESCRIPTION += '\n Link: \t\thttps://github.com/amis-shokoohi/kapak'

USAGE =    ' Usage:\t\tkapak [-e -d] <path> [-r]'
USAGE += '\n Example:\tkapak -e ./test.txt -r'
USAGE += '\n Help:\t\tkapak -h'

HELP_MESSAGE =    ' -h, --help\tShows this help message'
HELP_MESSAGE += '\n -e, --encrypt\tEncryption mode'
HELP_MESSAGE += '\n -d, --decrypt\tDecryption mode'
HELP_MESSAGE += '\n -r, --remove\tRemoves target file(s)'
HELP_MESSAGE += '\n path\t\tPath to file or directory'