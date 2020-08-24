from math import ceil

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
