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
		self.__percentage = 0
		self.__total_bytes_len = 0

	@staticmethod
	def get_instance():
		if not Progress.__instance:
			Progress()
		return Progress.__instance

	def set_total_size(self, total_bytes_len: int):
		self.__total_bytes_len = total_bytes_len

	def calc_percentage(self, read_bytes_len: int):
		p = read_bytes_len / self.__total_bytes_len
		self.__percentage += p * 100 if p <= 1 else 100

	def print_percentage(self):
		percentage = ceil(self.__percentage)
		i = floor(percentage / 10)
		print('\r' + 20*' ' + '\r' + self.__bar[i] + ' ' + str(percentage) + '%', end='')
