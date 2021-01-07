from lib.constants import BUFFER_SIZE

def pipeline(fd_in, fd_out, fn):
	while True:
		r_bytes = fd_in.read(BUFFER_SIZE)
		if r_bytes == b'':
			break
		w_bytes = fn(r_bytes)
		fd_out.write(w_bytes)