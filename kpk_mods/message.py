from kpk_mods.constants import USAGE, TITLE, HELP_MESSAGE, DESCRIPTION

def printDescription():
	print(TITLE)
	print(DESCRIPTION)
	print(' ------------------------------')
	print(USAGE + '\n')

def printHelp():
	print(TITLE)
	print(USAGE)
	print(' ------------------------------')
	print(HELP_MESSAGE + '\n')

def printUsage():
	print('\n' + USAGE + '\n')
