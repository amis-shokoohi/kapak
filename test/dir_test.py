import unittest
import os
import shutil
from pathlib import Path
import zipfile
import tempfile
from typing import List

from lib.dir import *

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

class TestDir_ContainsEncryptedFiles(unittest.TestCase):
	def setUp(self):
		self.temp_dir = Path(tempfile.mkdtemp())
		self.ee = ['', '.txt', '.tar.gz', '.kpk']
		data = b'abcdefghijklmnopqrstuvwxyz0123456789' # 36B
		for ext in self.ee:
			temp_fd, temp_fpath = tempfile.mkstemp(suffix=ext, dir=self.temp_dir)
			with open(temp_fpath, 'wb') as f:
				f.write(data)
			os.close(temp_fd)
		
	def test_contains_encrypted_files(self):
		self.assertTrue(contains_encrypted_files(self.temp_dir))
		f = list(self.temp_dir.rglob('*.kpk'))[0]
		os.remove(f)
		self.assertFalse(contains_encrypted_files(self.temp_dir))
		
	def tearDown(self):
		shutil.rmtree(self.temp_dir)

class TestDir_ZipDir(unittest.TestCase):
	def setUp(self):
		self.temp_dir = Path(tempfile.mkdtemp())
		self.ff: List[Path] = []
		data = b'abcdefghijklmnopqrstuvwxyz0123456789' # 36B
		for _ in range(5):
			temp_fd, temp_fpath = tempfile.mkstemp(dir=self.temp_dir)
			with open(temp_fpath, 'wb') as f:
				f.write(data)
			os.close(temp_fd)
			self.ff.append(Path(temp_fpath).relative_to(self.temp_dir.parent))

	def test_zip_dir(self):
		zp = zip_dir(self.temp_dir)
		self.assertTrue(zipfile.is_zipfile(zp))
		zff: List[Path] = []
		with zipfile.ZipFile(zp, mode='r') as zf:
			zff = [Path(f) for f in zf.namelist()]
		self.assertEqual(len(zff), len(self.ff))
		for f in self.ff:
			self.assertTrue(
				f in zff, 
				msg=str(f) + ' does not exist in ' + ', \n'.join([str(zf) for zf in zff])
			)
		zp.unlink()

	def tearDown(self):
		shutil.rmtree(self.temp_dir)

class TestDir_ZipDir2(unittest.TestCase):
	def setUp(self):
		curr_dir = os.getcwd()
		self.temp_dir = Path(Path(tempfile.mkdtemp(dir=curr_dir)).name)
		self.ff: List[Path] = []
		data = b'abcdefghijklmnopqrstuvwxyz0123456789' # 36B
		for _ in range(5):
			temp_fd, temp_fpath = tempfile.mkstemp(dir=self.temp_dir)
			with open(temp_fpath, 'wb') as f:
				f.write(data)
			os.close(temp_fd)
			self.ff.append(Path(temp_fpath).relative_to(self.temp_dir.resolve().parent))

	def test_zip_dir(self):
		zp = zip_dir(self.temp_dir)
		self.assertTrue(zipfile.is_zipfile(zp))
		zff: List[Path] = []
		with zipfile.ZipFile(zp, mode='r') as zf:
			zff = [Path(f) for f in zf.namelist()]
		self.assertEqual(len(zff), len(self.ff))
		for f in self.ff:
			self.assertTrue(
				f in zff, 
				msg=str(f) + ' does not exist in ' + ', \n'.join([str(zf) for zf in zff])
			)
		zp.unlink()

	def tearDown(self):
		shutil.rmtree(self.temp_dir)

class TestDir_UnzipDir(unittest.TestCase):
	def setUp(self):
		self.temp_dir = Path(tempfile.mkdtemp())
		self.ff: List[Path] = []
		data = b'abcdefghijklmnopqrstuvwxyz0123456789' # 36B
		for _ in range(5):
			temp_fd, temp_fpath = tempfile.mkstemp(dir=self.temp_dir)
			with open(temp_fpath, 'wb') as f:
				f.write(data)
			os.close(temp_fd)
			self.ff.append(Path(temp_fpath))
		self.zp = zip_dir(self.temp_dir)
		shutil.rmtree(self.temp_dir)

	def test_unzip_dir(self):
		unzip_dir(self.zp)
		self.assertTrue(os.path.isdir(self.temp_dir))
		uzff = list(self.temp_dir.rglob('*'))
		for f in self.ff:
			self.assertTrue(
				f in uzff,
				msg=str(f) + ' does not exist in ' + ', \n'.join([str(uzf) for uzf in uzff])
			)

	def tearDown(self):
		shutil.rmtree(self.temp_dir)
		self.zp.unlink()
