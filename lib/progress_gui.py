from lib.progress import Progress

class ProgressGUI(Progress):
	def __init__(self, total_bytes_len: int, window):
		super().__init__(total_bytes_len)
		self._window = window
	
	def print(self):
		self._window.evaluate_js(fr"showProgress({self._percentage})")
