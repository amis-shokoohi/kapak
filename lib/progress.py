import sys
from math import ceil, floor

class Progress:
	_bar = [
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

	def __init__(self, total_bytes_len: int):
		self._total_bytes_len = total_bytes_len
		self._processed_bytes_len = 0
		self._percentage = 0

	def update(self, bytes_len: int):
		self._processed_bytes_len += bytes_len
		p = ceil(self._processed_bytes_len / self._total_bytes_len * 100)
		self._percentage = p if p <= 100 else 100

	def print(self):
		i = floor(self._percentage / 10)
		print('\r' + 20*' ' + '\r' + self._bar[i] + ' ' + str(self._percentage) + '%', end='')
		sys.stdout.flush()
