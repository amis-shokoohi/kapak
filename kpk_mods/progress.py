from os import path, stat

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
	i = int(percentage / 10)
	if percentage >= 100:
		i = 10

	print('\r ' + progress[i] + ' ' + str(int(percentage)) + '%', end='')

def showProgressComplete():
	print('\r [■■■■■■■■■■] 100%\n')

percentage = 0
def calcPercentage(read_bytes, total_bytes):
	global percentage
	percentage += read_bytes * 100 / total_bytes
	return percentage
