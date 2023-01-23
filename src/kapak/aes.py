from os import urandom
from functools import partial
from hashlib import sha256
from typing import Generator, BinaryIO

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from kapak.version import __version__
from kapak.key import derive_key
from kapak.error import KapakError


BUFFER_SIZE = 64 * 1024
AES_BLOCK_SIZE = 16
SALT_SIZE = 16
VERIFIER_SIZE = 16
VERIFIER_HASH_SIZE = 32


def encrypt(
    src: BinaryIO, dst: BinaryIO, password: str, buffer_size: int = BUFFER_SIZE
) -> Generator[int, None, None]:
    if buffer_size % AES_BLOCK_SIZE != 0:
        raise KapakError("buffer size must be a multiple of aes-block-size (16 bytes)")

    salt = urandom(SALT_SIZE)
    key = derive_key(password, salt)

    iv = urandom(AES_BLOCK_SIZE)
    encryptor = Cipher(
        algorithms.AES(key), modes.CBC(iv), backend=default_backend()
    ).encryptor()

    major_version = int(__version__.split(".")[0]).to_bytes(4, "big")

    salt_size = SALT_SIZE.to_bytes(4, "big")

    # This is just a quick way to inform user that the entered password is wrong in decryption phase.
    # This does not check authenticity or integrity of the encrypted file by any means.
    verifier = urandom(VERIFIER_SIZE)
    verifier_hash = sha256(verifier)
    encrypted_verifier = encryptor.update(verifier)
    verifier_size = VERIFIER_SIZE.to_bytes(4, "big")
    encrypted_verifier_hash = encryptor.update(verifier_hash.digest())
    verifier_hash_size = VERIFIER_HASH_SIZE.to_bytes(4, "big")

    reserved_size = int(0).to_bytes(4, "big")

    header = (
        b"kapak"
        + major_version
        + iv
        + salt_size
        + salt
        + verifier_size
        + encrypted_verifier
        + verifier_hash_size
        + encrypted_verifier_hash
        + reserved_size
        + reserved_size
    )
    header_length = len(header).to_bytes(4, "big")
    header = header_length + header

    dst.write(header)

    for chunk in iter(partial(src.read, buffer_size), b""):
        chunk_len = len(chunk)
        chunk = _pad_bytes(chunk)
        chunk = encryptor.update(chunk)
        dst.write(chunk)
        yield chunk_len
    dst.write(encryptor.finalize())


class Header:
    def __init__(self, header: bytes) -> None:
        self.header = header
        self._cursor = 0

    def read(self, length: int) -> bytes:
        current_position = self._cursor
        self._cursor += length
        return self.header[current_position : self._cursor]


def decrypt(
    src: BinaryIO, dst: BinaryIO, password: str, buffer_size: int = BUFFER_SIZE
) -> Generator[int, None, None]:
    if buffer_size % AES_BLOCK_SIZE != 0:
        raise KapakError("buffer size must be a multiple of aes-block-size (16 bytes)")

    header_length = int.from_bytes(src.read(4), "big")
    header = Header(src.read(header_length))
    yield 4 + header_length

    if header.read(5) != b"kapak":
        raise KapakError("not able to decrypt this file format")

    # Check version
    src_mv = int.from_bytes(header.read(4), "big")
    mv = int(__version__.split(".")[0])
    if src_mv != mv:
        raise KapakError("source version does not match the current version of Kapak")

    iv = header.read(AES_BLOCK_SIZE)
    salt_size = int.from_bytes(header.read(4), "big")
    salt = header.read(salt_size)
    key = derive_key(password, salt)
    decryptor = Cipher(
        algorithms.AES(key), modes.CBC(iv), backend=default_backend()
    ).decryptor()

    # Check key
    # This is just a quick way to inform user that the entered password is wrong.
    # This does not check authenticity or integrity of the encrypted file by any means.
    verifier_size = int.from_bytes(header.read(4), "big")
    encrypted_verifier = header.read(verifier_size)
    verifier = decryptor.update(encrypted_verifier)
    verifier_hash_size = int.from_bytes(header.read(4), "big")
    encrypted_verifier_hash = header.read(verifier_hash_size)
    verifier_hash = decryptor.update(encrypted_verifier_hash)
    if sha256(verifier).digest() != verifier_hash:
        raise KapakError("wrong password")

    for chunk in iter(partial(src.read, buffer_size), b""):
        chunk_len = len(chunk)
        chunk = decryptor.update(chunk)
        chunk = _unpad_bytes(chunk)
        dst.write(chunk)
        yield chunk_len
    dst.write(decryptor.finalize())


def _pad_bytes(bytes_in: bytes) -> bytes:
    if len(bytes_in) % AES_BLOCK_SIZE == 0:
        return bytes_in
    padder = padding.PKCS7(AES_BLOCK_SIZE * 8).padder()
    padded: bytes = padder.update(bytes_in) + padder.finalize()
    return padded


def _unpad_bytes(bytes_in: bytes) -> bytes:
    unpadder = padding.PKCS7(AES_BLOCK_SIZE * 8).unpadder()
    try:
        unpadded: bytes = unpadder.update(bytes_in) + unpadder.finalize()
        return unpadded
    except ValueError:
        return bytes_in
