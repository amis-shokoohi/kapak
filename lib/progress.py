from math import ceil, floor
from typing import Callable

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

	def __init__(self, is_gui=False):
		if Progress.__instance:
			raise Exception("not able to create another instance from Progress")
		Progress.__instance = self
		self.__processed_bytes_len = 0
		self.__total_bytes_len = 0
		self.__percentage = 0
		self.__is_gui = is_gui

	@staticmethod
	def get_instance():
		if not Progress.__instance:
			Progress()
		return Progress.__instance

	def set_total_size(self, total_bytes_len: int):
		self.__total_bytes_len = total_bytes_len

	def set_print_fn(self, print_fn: Callable):
		self.__print_gui = print_fn

	def update(self, bytes_len: int):
		self.__processed_bytes_len += bytes_len
		p = ceil(self.__processed_bytes_len / self.__total_bytes_len * 100)
		self.__percentage = p if p <= 100 else 100

	def print(self):
		if self.__is_gui:
			self.__print_gui(self.__percentage)
			return
		i = floor(self.__percentage / 10)
		print('\r' + 20*' ' + '\r' + self.__bar[i] + ' ' + str(self.__percentage) + '%', end='')
	
	def reset(self):
		self.__processed_bytes_len = 0
		self.__total_bytes_len = 0
		self.__percentage = 0
