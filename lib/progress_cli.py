from math import floor
import sys

from lib.progress import Progress

class ProgressCLI(Progress):
	def __init__(self, total_bytes_len: int):
		super().__init__(total_bytes_len)
		self._bar = [
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

	def print(self):
		i = floor(self._percentage / 10)
		print('\r' + 20*' ' + '\r' + self._bar[i] + ' ' + str(self._percentage) + '%', end='')
		sys.stdout.flush()
