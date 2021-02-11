from typing import Callable, BinaryIO
from functools import partial

def new_pipeline(buffer_size: int) -> Callable:
	def pipeline(
		fd_in: BinaryIO, 
		op1: Callable[[bytes], bytes],
		op2: Callable[[bytes], bytes],
		op3: Callable[[bytes], bytes],
		fd_out: BinaryIO):
		for chunk in iter(partial(fd_in.read, buffer_size), b''):
			chunk = op1(chunk)
			chunk = op2(chunk)
			chunk = op3(chunk)
			fd_out.write(chunk)
	return pipeline
