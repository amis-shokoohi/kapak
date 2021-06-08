import unittest
import os
import shutil
from pathlib import Path
import zipfile
import tempfile
from typing import List

from lib.dir import calc_total_size, zip_dir, unzip_dir

class TestDir_CalcTotalSize(unittest.TestCase):
	def setUp(self):
		self.expected_total_size = 0
		self.ff: List[Path] = []
		self.temp_dir = Path(tempfile.mkdtemp())
		data = b'abcdefghijklmnopqrstuvwxyz0123456789' # 36B
		for _ in range(5):
			temp_fd, temp_fpath = tempfile.mkstemp(dir=self.temp_dir)
			with open(temp_fpath, 'wb') as f:
				f.write(data)
			os.close(temp_fd)
			self.expected_total_size += len(data)
			self.ff.append(Path(temp_fpath))
			
	def test_calc_total_size(self):
		self.assertEqual(calc_total_size(self.ff), self.expected_total_size)

	def tearDown(self):
		shutil.rmtree(self.temp_dir)

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
