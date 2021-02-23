from pathlib import Path
import os
import shutil
import sys

import webview

from lib.file_extension import file_ext, replace_file_ext
from lib.progress import Progress
from lib.passwd import derive_key
from lib.constants import BUFFER_SIZE, ENCRYPT_MODE, TEMP_ZIP_EXT, DECRYPT_MODE
from lib.dir import zip_dir, unzip_dir, list_files, calc_total_size
import lib.encryptor
import lib.decryptor

class App():
	def __init__(self):
		self.buffer_size = BUFFER_SIZE * 1024 * 1024
		self.path = Path('')
		self.progress = Progress(True)
		self.progress.set_print_fn(self.js_show_progress)

	def open_file_dialog(self):
		result = window.create_file_dialog()
		self.path = Path(result[0])
		return result[0]

	def open_folder_dialog(self):
		result = window.create_file_dialog(webview.FOLDER_DIALOG)
		self.path = Path(result[0])
		return result[0]

	def js_enable_form(self):
		window.evaluate_js(fr"enableForm()")

	def js_reset_encrypt_form(self):
		window.evaluate_js(fr"resetForm('form-encrypt')")

	def js_reset_decrypt_form(self):
		window.evaluate_js(fr"resetForm('form-decrypt')")

	def js_log_msg(self, msg):
		window.evaluate_js(fr"logMsg('{msg}')")

	def js_log_error(self, err):
		window.evaluate_js(fr"logError('{err}')")

	def js_show_progress(self, percentage):
		window.evaluate_js(fr"showProgress({percentage})")

	def js_clear_logs(self):
		window.evaluate_js(fr"clearLogs()")

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
			self.progress.set_total_size(target_size)

			self.js_log_msg('Encrypting...')
			key, salt = derive_key(password, None)
			lib.encryptor.encrypt(key, salt, self.path, self.buffer_size)

			if should_remove:
				os.remove(self.path)
				
			self.path = Path('')
			self.js_reset_encrypt_form()
			self.js_log_msg('Done')
		except Exception as err:
			self.js_clear_logs()
			self.js_log_error(err.args[0])
		finally:
			self.progress.reset()
			self.js_enable_form()
	
	def zip_folder_then_encrypt(self, password, should_remove):
		try:
			self.validate_entries(password)

			f_out_name = Path(str(self.path) + '.kpk')
			if os.path.exists(f_out_name): # Overwrite error
				raise Exception(f_out_name.name + ' already exists')

			self.js_log_msg('Zipping...')
			zp = zip_dir(self.path) # Creates a temporary zip file
			target_size = os.stat(zp).st_size
			if target_size == 0:
				raise Exception(self.path.name + ' is empty')
			self.progress.set_total_size(target_size)

			self.js_log_msg('Encrypting...')
			key, salt = derive_key(password, None)
			lib.encryptor.encrypt(key, salt, zp, self.buffer_size)
			os.remove(zp)

			if should_remove:
				shutil.rmtree(self.path)

			self.path = Path('')
			self.js_reset_encrypt_form()
			self.js_log_msg('Done')
		except Exception as err:
			self.js_clear_logs()
			self.js_log_error(err.args[0])
		finally:
			self.progress.reset()
			self.js_enable_form()

	def encrypt_folder(self, password, should_remove):
		try:
			self.validate_entries(password)

			self.js_log_msg('Looking for files in the directory...')
			ff = list_files(self.path, ENCRYPT_MODE) # List of files in the directory
			if len(ff) == 0:
				raise Exception(self.path.name + ' is empty')
			target_size = calc_total_size(ff)
			if target_size == 0:
				raise Exception(self.path.name + ' is empty')
			self.progress.set_total_size(target_size)

			self.js_log_msg('Encrypting...')
			key, salt = derive_key(password, None)
			for f in ff:
				f_out_name = replace_file_ext(f, 'kpk')
				if os.path.exists(f_out_name): # Overwrite error
					raise Exception(f_out_name.name + ' already exists')
				lib.encryptor.encrypt(key, salt, f, self.buffer_size)
				if should_remove:
					os.remove(f)

			self.path = Path('')
			self.js_reset_encrypt_form()
			self.js_log_msg('Done')
		except Exception as err:
			self.js_clear_logs()
			self.js_log_error(err.args[0])
		finally:
			self.progress.reset()
			self.js_enable_form()

	def decrypt_file(self, password, should_remove):
		try:
			self.validate_entries(password)

			if file_ext(self.path) != 'kpk':
				raise Exception('can not decrypt ' + self.path.name)

			target_size = os.stat(self.path).st_size
			if target_size == 0:
				raise Exception(self.path.name + ' is empty')
			self.progress.set_total_size(target_size)

			self.js_log_msg('Decrypting...')
			f_out_path, f_out_ext = lib.decryptor.decrypt(password, self.path, self.buffer_size)
			if f_out_ext == TEMP_ZIP_EXT:
				unzip_dir(f_out_path)
				os.remove(f_out_path)

			if should_remove:
				os.remove(self.path)

			self.path = Path('')
			self.js_reset_decrypt_form()
			self.js_log_msg('Done')
		except Exception as err:
			self.js_clear_logs()
			self.js_log_error(err.args[0])
		finally:
			self.progress.reset()
			self.js_enable_form()

	def decrypt_folder(self, password, should_remove):
		try:
			self.validate_entries(password)

			self.js_log_msg('Decrypting...')
			ff = list_files(self.path, DECRYPT_MODE) # List of files in the directory
			if len(ff) == 0:
				raise Exception(self.path.name + ' is empty')

			target_size = calc_total_size(ff)
			if target_size == 0:
				raise Exception(self.path.name + ' is empty')
			self.progress.set_total_size(target_size)

			for f in ff:
				_, _ = lib.decryptor.decrypt(password, f, self.buffer_size)
				if should_remove:
					os.remove(f)

			self.path = Path('')
			self.js_reset_decrypt_form()
			self.js_log_msg('Done')
		except Exception as err:
			self.js_clear_logs()
			self.js_log_error(err.args[0])
		finally:
			self.progress.reset()
			self.js_enable_form()

if __name__ == '__main__':
	base_dir = os.path.dirname(os.path.realpath(__file__))

	# Code to fix pyinstaller problem with finding view directory
	if hasattr(sys, '_MEIPASS'):
		base_dir = sys._MEIPASS

	view_path = Path(os.path.join(base_dir, 'view/index.html'))
	assert os.path.exists(view_path), 'not able to find view directory'

	app = App()
	window = webview.create_window(
		title='kapak', url=view_path, js_api=app,
		width=400, height=580, resizable=False
	)
	webview.start(http_server=True)