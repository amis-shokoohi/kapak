import unittest

from lib.encryptor import _pad_bytes

class TestEncryptor_PadBytes(unittest.TestCase):
	def test_pad_bytes(self):
		b1 = b''
		self.assertTrue(len(_pad_bytes(b1)) == 0)
		b2 = bytes(''.zfill(15), 'utf-8')
		self.assertTrue(len(_pad_bytes(b2)) % 16 == 0)
		b3 = bytes(''.zfill(16), 'utf-8')
		self.assertTrue(len(_pad_bytes(b3)) % 16 == 0)
		b4 = bytes(''.zfill(17), 'utf-8')
		self.assertTrue(len(_pad_bytes(b4)) % 16 == 0)
		print(_pad_bytes(b4))