from os import path, stat
from math import ceil

def getTotalSize(fList):
	totalSize = 1
	for f in fList:
		if path.isdir(f):
			continue
		totalSize += stat(f).st_size
	return totalSize

progress = [
	'[□□□□□□□□□□]',
	'[■□□□□□□□□□]',
	'[■■□□□□□□□□]',
	'[■■■□□□□□□□]',
	'[■■■■□□□□□□]',
	'[■■■■■□□□□□]',
	'[■■■■■■□□□□]',
	'[■■■■■■■□□□]',
	'[■■■■■■■■□□]',
	'[■■■■■■■■■□]',
	'[■■■■■■■■■■]'
]

def showProgress(percentage):
	i = ceil(percentage / 10)
	if percentage > 99.8:
		print('\r [■■■■■■■■■■] 100%\n')
		return

	print('\r ' + progress[i] + ' ' + str(int(percentage)) + '%', end='')

percentage = 0
def calcPercentage(read_bytes, total_bytes):
	global percentage
	percentage += read_bytes * 100 / total_bytes
	return percentage
