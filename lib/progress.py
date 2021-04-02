from math import ceil

class Progress:
	def __init__(self, total_bytes_len: int):
		self._total_bytes_len = total_bytes_len
		self._processed_bytes_len = 0
		self._percentage = 0

	def update(self, bytes_len: int):
		self._processed_bytes_len += bytes_len
		p = ceil(self._processed_bytes_len / self._total_bytes_len * 100)
		self._percentage = p if p <= 100 else 100
