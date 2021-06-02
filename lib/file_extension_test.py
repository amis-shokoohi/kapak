import unittest
from pathlib import Path

from lib.file_extension import file_ext, replace_file_ext

class TestFileExtension(unittest.TestCase):
	def test_file_ext(self):
		p1 = Path('path/to/file.txt')
		self.assertEqual(file_ext(p1), 'txt')
		p2 = Path('path/to/file')
		self.assertEqual(file_ext(p2), '')
		p3 = Path('path/to/file.tar.gz')
		self.assertEqual(file_ext(p3), 'gz')

	def test_replace_file_ext(self):
		p1 = Path('path/to/file.txt')
		self.assertEqual(replace_file_ext(p1, 'kpk'), Path('path/to/file.kpk'))
		p2 = Path('path/to/file.tar.gz')
		self.assertEqual(replace_file_ext(p2, 'kpk'), Path('path/to/file.tar.kpk'))
		p3 = Path('path/to/file')
		self.assertEqual(replace_file_ext(p3, 'kpk'), Path('path/to/file.kpk'))
		p4 = Path('path/to/file.kpk')
		self.assertEqual(replace_file_ext(p4, ''), Path('path/to/file'))
		p5 = Path('path/to/file')
		self.assertEqual(replace_file_ext(p5, ''), Path('path/to/file'))
