from math import ceil, floor

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
	percentage = ceil(percentage)
	i = floor(percentage / 10)
	eraser = '\r' + 20*' '
	print(eraser + '\r ' + progress[i] + ' ' + str(percentage) + '%', end='')

percentage = 0
def calcPercentage(read_bytes, total_bytes):
	global percentage
	percentage += read_bytes * 100 / total_bytes
	return percentage
