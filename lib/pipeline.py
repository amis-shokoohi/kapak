from lib.constants import BUFFER_SIZE
from typing import Callable, BinaryIO

def pipeline(fd_in: BinaryIO, fd_out: BinaryIO, fn: Callable[[bytes], bytes]):
	while True:
		r_bytes = fd_in.read(BUFFER_SIZE)
		if r_bytes == b'':
			break
		w_bytes = fn(r_bytes)
		fd_out.write(w_bytes)