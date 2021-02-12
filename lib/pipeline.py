from typing import Callable, BinaryIO
from functools import partial

from lib.progress import Progress

def new_pipeline(buffer_size: int) -> Callable:
	def pipeline(
		fd_in: BinaryIO, 
		op1: Callable[[bytes], bytes],
		op2: Callable[[bytes], bytes],
		fd_out: BinaryIO):
		progress = Progress.get_instance()
		for chunk in iter(partial(fd_in.read, buffer_size), b''):
			progress.update(len(chunk))
			chunk = op1(chunk)
			chunk = op2(chunk)
			fd_out.write(chunk)
			progress.print()
	return pipeline
