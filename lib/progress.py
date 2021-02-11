from math import ceil, floor

class Progress:
	__instance = None
	__bar = [
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

	def __init__(self):
		if Progress.__instance:
			raise Exception("not able to create another instance from Progress")
		Progress.__instance = self
		self.__processed_bytes_len = 0
		self.__total_bytes_len = 0

	@staticmethod
	def get_instance():
		if not Progress.__instance:
			Progress()
		return Progress.__instance

	def set_total_size(self, total_bytes_len: int):
		self.__total_bytes_len = total_bytes_len

	def update(self, bytes_in: bytes) -> bytes:
		self.__processed_bytes_len += len(bytes_in)
		self.__print()
		return bytes_in

	def __print(self):
		p = ceil(self.__processed_bytes_len / self.__total_bytes_len * 100)
		percentage = p if p <= 100 else 100
		i = floor(percentage / 10)
		print('\r' + 20*' ' + '\r' + self.__bar[i] + ' ' + str(percentage) + '%', end='')
