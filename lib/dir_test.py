import unittest
import os
import shutil
from pathlib import Path
import zipfile

from lib.dir import calc_total_size, list_files, zip_dir, unzip_dir
from lib.constants import ENCRYPT_MODE, DECRYPT_MODE, TEMP_ZIP_EXT

class TestDir_CalcTotalSize(unittest.TestCase):
	def setUp(self):
		self.ff = []
		self.temp_dir_name = Path('temp-test-dir-cts')
		os.mkdir(self.temp_dir_name)
		for i in range(5):
			temp_file_path = self.temp_dir_name / Path('temp_test_file_' + str(i + 1) + '.dat')
			with open(temp_file_path, 'wb') as f:
				f.write(b'abcdefghijklmnopqrstuvwxyz0123456789') # 36B
			self.ff.append(temp_file_path)
			
	def test_calc_total_size(self):
		expected_size = 5 * 36
		self.assertEqual(calc_total_size(self.ff), expected_size)

	def tearDown(self):
		shutil.rmtree(self.temp_dir_name)

class TestDir_ListFiles(unittest.TestCase):
	def setUp(self):
		self.temp_dir_name = Path('temp-test-dir-lf')
		self.file_list = [
			self.temp_dir_name / Path('temp_test_file_1.dat'),
			self.temp_dir_name / Path('temp_test_file_2.kpk'),
			self.temp_dir_name / Path('temp_test_file_3.txt'),
			self.temp_dir_name / Path('temp_test_file_4.kpk')
		]
		os.mkdir(self.temp_dir_name)
		for file_path in self.file_list:
			f = open(file_path, 'wb')
			f.close()

	def test_list_files(self):
		expected_file_list_enc = [
			self.temp_dir_name / Path('temp_test_file_1.dat'),
			self.temp_dir_name / Path('temp_test_file_3.txt')
		]
		ff_enc = list_files(self.temp_dir_name, ENCRYPT_MODE)
		self.assertEqual(len(ff_enc), len(expected_file_list_enc))
		for f in expected_file_list_enc:
			self.assertTrue(f in ff_enc)

		expected_file_list_dec = [
			self.temp_dir_name / Path('temp_test_file_2.kpk'),
			self.temp_dir_name / Path('temp_test_file_4.kpk')
		]
		ff_dec = list_files(self.temp_dir_name, DECRYPT_MODE)
		self.assertEqual(len(ff_dec), len(expected_file_list_dec))
		for f in expected_file_list_dec:
			self.assertTrue(f in ff_dec)

	def tearDown(self):
		shutil.rmtree(self.temp_dir_name)

class TestDir_ZipDir(unittest.TestCase):
	def setUp(self):
		self.ff = []
		self.temp_dir_name = Path('temp-test-dir-z')
		os.mkdir(self.temp_dir_name)
		for i in range(5):
			temp_file_path = self.temp_dir_name / Path('temp_test_file_' + str(i + 1) + '.dat')
			with open(temp_file_path, 'wb') as f:
				f.write(b'abcdefghijklmnopqrstuvwxyz0123456789') # 36B
			self.ff.append(temp_file_path)

	def test_zip_dir(self):
		zp = zip_dir(self.temp_dir_name)
		self.assertTrue(zipfile.is_zipfile(zp))
		with zipfile.ZipFile(zp, mode='r') as zf:
			self.assertListEqual([Path(f) for f in sorted(zf.namelist())], self.ff)
		os.remove(zp)

	def tearDown(self):
		shutil.rmtree(self.temp_dir_name)

class TestDir_ZipDir2(unittest.TestCase):
	def setUp(self):
		self.temp_dir_name = Path('temp-test-dir-z2')
		os.mkdir(self.temp_dir_name)

		self.inner_temp_dir_name = Path('inner_temp-test-dir-z2')
		self.inner_temp_dir_path = self.temp_dir_name / self.inner_temp_dir_name
		os.mkdir(self.inner_temp_dir_path)

		self.ff = []
		for i in range(5):
			temp_file_name = Path('temp_test_file_' + str(i + 1) + '.dat')
			temp_file_path = self.inner_temp_dir_path / temp_file_name
			with open(temp_file_path, 'wb') as f:
				f.write(b'abcdefghijklmnopqrstuvwxyz0123456789') # 36B
			self.ff.append(self.inner_temp_dir_name / temp_file_name)

	def test_zip_dir(self):
		zp = zip_dir(self.inner_temp_dir_path)
		self.assertTrue(zipfile.is_zipfile(zp))
		with zipfile.ZipFile(zp, mode='r') as zf:
			self.assertListEqual([Path(f) for f in sorted(zf.namelist())], self.ff)
		os.remove(zp)

	def tearDown(self):
		shutil.rmtree(self.temp_dir_name)

class TestDir_UnzipDir(unittest.TestCase):
	def setUp(self):
		self.ff = []
		self.temp_dir_name = Path('temp-test-dir-u')
		os.mkdir(self.temp_dir_name)
		for i in range(5):
			temp_file_path = self.temp_dir_name / Path('temp_test_file_' + str(i + 1) + '.dat')
			with open(temp_file_path, 'wb') as f:
				f.write(b'abcdefghijklmnopqrstuvwxyz0123456789') # 36B
			self.ff.append(temp_file_path)
		self.zp = zip_dir(self.temp_dir_name)
		shutil.rmtree(self.temp_dir_name)

	def test_unzip_dir(self):
		unzip_dir(self.zp)
		self.assertTrue(os.path.isdir(self.temp_dir_name))
		self.assertListEqual(sorted(list(self.temp_dir_name.rglob('*'))), self.ff)

	def tearDown(self):
		shutil.rmtree(self.temp_dir_name)
		os.remove(self.zp)
