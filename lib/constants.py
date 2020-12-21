BUFFER_SIZE = 64 * 1024 * 1024 # 64MB
TEMP_ZIP_EXT = 'kpktempzip'

ENCRYPT_MODE = 1
DECRYPT_MODE = 2

_VERSION = 'v2.2.0'
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

USAGE =    ' Usage:\t\tkapak [options] <path>'
USAGE += '\n Example:\tkapak -e -r test.txt'
USAGE += '\n Help:\t\tkapak -h'

HELP_MESSAGE =    ' -h, --help\tShows this help message'
HELP_MESSAGE += '\n -e, --encrypt\tEncryption mode'
HELP_MESSAGE += '\n -d, --decrypt\tDecryption mode'
HELP_MESSAGE += '\n -r, --remove\tRemoves the target file(s)'
HELP_MESSAGE += '\n -z, --zip\tZips a directory before encryption'
HELP_MESSAGE += '\n path\t\tPath to a file or a directory'