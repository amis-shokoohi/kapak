from pathlib import Path
import os
import shutil

import webview

# import lib.gui_encrypt
# import lib.gui_decrypt
from lib.file_exntension import file_ext, replace_file_ext
from lib.progress import Progress
from lib.passwd import derive_key
import lib.encryptor
from lib.constants import BUFFER_SIZE, ENCRYPT_MODE
from lib.dir import zip_dir, list_files, calc_total_size

class App():
	def __init__(self):
		self.path = Path('')

	def open_file_dialog(self):
		result = window.create_file_dialog()
		self.path = Path(result[0])
		return result[0]

	def open_folder_dialog(self):
		result = window.create_file_dialog(webview.FOLDER_DIALOG)
		self.path = Path(result[0])
		return result[0]

	def js_show_error(self, msg):
		window.evaluate_js(fr'''
			const duration = 3000;
			const card = document.createElement('div');
			card.innerText = 'Error: ' + '{msg}';
			card.classList.add('err-card');
			const logo = document.getElementById('logo');
			document.body.insertBefore(card, logo);
			setTimeout(() => card.style.top = '3rem', 100);
			setTimeout(() => card.style.top = '-3rem', duration);
			setTimeout(() => card.remove(), duration + 200);
		''')

	def validate_entries(self, password):
		if self.path == Path(''):
			raise Exception('no file/folder chosen')
		if not os.path.exists(self.path):
			raise Exception('can not find ' + self.path.name)

		if password == '' or len(password) < 3 or len(password) > 1024:
			raise Exception('password should be at least 3 characters')

	def encrypt_file(self, password, should_remove):
		try:
			self.validate_entries(password)
			
			if file_ext(self.path) == 'kpk':
				raise Exception('can not encrypt ' + self.path.name)

			f_out_name = replace_file_ext(self.path, 'kpk')
			if os.path.exists(f_out_name): # Overwrite error
				raise Exception(f_out_name.name + ' already exists')

			target_size = os.stat(self.path).st_size
			if target_size == 0:
				raise Exception(self.path.name + ' is empty')

			progress = Progress()
			progress.set_total_size(target_size)
			key, salt = derive_key(password, None)
			lib.encryptor.encrypt(key, salt, self.path, BUFFER_SIZE * 1024 * 1024)

			if should_remove:
				os.remove(self.path)
		except Exception as err:
			self.js_show_error(err.args[0])
	
	def zip_folder_then_encrypt(self, password, should_remove):
		try:
			self.validate_entries(password)

			f_out_name = str(self.path) + '.kpk'
			if os.path.exists(f_out_name): # Overwrite error
				raise Exception(f_out_name + ' already exists')

			zp = zip_dir(self.path) # Creates a temporary zip file
			target_size = os.stat(zp).st_size
			if target_size == 0:
				raise Exception(self.path.name + ' is empty')

			progress = Progress()
			progress.set_total_size(target_size)
			key, salt = derive_key(password, None)
			lib.encryptor.encrypt(key, salt, zp, BUFFER_SIZE * 1024 * 1024)
			os.remove(zp)

			if should_remove:
				shutil.rmtree(self.path)
		except Exception as err:
			self.js_show_error(err.args[0])

	def encrypt_folder(self, password, should_remove):
		try:
			self.validate_entries(password)

			ff = list_files(self.path, ENCRYPT_MODE) # List of files in the directory
			if len(ff) == 0:
				raise Exception(self.path.name + ' is empty')
			target_size = calc_total_size(ff)
			if target_size == 0:
				raise Exception(self.path.name + ' is empty')

			progress = Progress()
			progress.set_total_size(target_size)
			key, salt = derive_key(password, None)
			for f in ff:
				f_out_name = replace_file_ext(f, 'kpk')
				if os.path.exists(f_out_name): # Overwrite error
					raise Exception(f_out_name.name + ' already exists')
				lib.encryptor.encrypt(key, salt, f, BUFFER_SIZE * 1024 * 1024)
				if should_remove:
					os.remove(f)
		except Exception as err:
			self.js_show_error(err.args[0])

	def decrypt_folder(self, password, should_remove):
		print('decrypt folder')

	def decrypt_file(self, password, should_remove):
		print('decrypt file')

if __name__ == '__main__':
	app = App()
	window = webview.create_window(
		title='KapaK', url='./view/', js_api=app,
		width=400, height=600, resizable=False
	)
	webview.start()