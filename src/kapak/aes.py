from os import urandom
from pathlib import Path
from functools import partial
from hashlib import sha256
from typing import Generator

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from kapak.version import __version__
from kapak.key import derive_key
from kapak.error import KapakError


AES_BLOCK_SIZE = 16


def encrypt(
    src: Path, dest: Path, key: bytes, salt: bytes, buffer_size: int
) -> Generator[int, None, None]:
    iv = urandom(AES_BLOCK_SIZE)
    encryptor = Cipher(
        algorithms.AES(key), modes.CBC(iv), backend=default_backend()
    ).encryptor()

    verifier = urandom(16)
    verifier_hash = sha256(verifier)
    encrypted_verifier = encryptor.update(verifier)
    encrypted_verifier_hash = encryptor.update(verifier_hash.digest())

    ext = src.suffix
    encrypted_ext = encryptor.update(_pad_bytes(bytes(ext, "utf-8")))

    major_version = int(__version__.split(".")[0]).to_bytes(4, "big")

    header = (
        major_version
        + iv
        + salt
        + encrypted_verifier
        + encrypted_verifier_hash
        + encrypted_ext
    )
    header_length = len(header).to_bytes(4, "big")

    with src.open("rb") as src_, dest.open("wb") as dest_:
        # Write header
        dest_.write(header_length + header)

        for chunk in iter(partial(src_.read, buffer_size), b""):
            chunk_len = len(chunk)
            chunk = _pad_bytes(chunk)
            chunk = encryptor.update(chunk)
            dest_.write(chunk)
            yield chunk_len
        dest_.write(encryptor.finalize())


def _pad_bytes(bytes_in: bytes) -> bytes:
    if len(bytes_in) % AES_BLOCK_SIZE == 0:
        return bytes_in
    padder = padding.PKCS7(AES_BLOCK_SIZE * 8).padder()
    padded: bytes = padder.update(bytes_in) + padder.finalize()
    return padded


def decrypt(src: Path, password: str, buffer_size: int) -> Generator[int, None, None]:
    with src.open("rb") as src_:
        header_length = int.from_bytes(src_.read(4), "big")
        header = src_.read(header_length)
        yield 4 + header_length

        # Check version
        src_mv = int.from_bytes(header[0:4], "big")
        mv = int(__version__.split(".")[0])
        if src_mv != mv:
            raise KapakError(f"need an older version of Kapak to decrypt {src}")

        iv = header[4 : 4 + AES_BLOCK_SIZE]
        salt = header[4 + AES_BLOCK_SIZE : 20 + AES_BLOCK_SIZE]
        key = derive_key(password, salt)
        decryptor = Cipher(
            algorithms.AES(key), modes.CBC(iv), backend=default_backend()
        ).decryptor()

        # Verify key
        encrypted_verifier = header[20 + AES_BLOCK_SIZE : 36 + AES_BLOCK_SIZE]
        verifier = decryptor.update(encrypted_verifier)
        encrypted_verifier_hash = header[36 + AES_BLOCK_SIZE : 68 + AES_BLOCK_SIZE]
        verifier_hash = decryptor.update(encrypted_verifier_hash)
        if sha256(verifier).digest() != verifier_hash:
            raise KapakError("wrong password")

        # Decrypt file extension
        encrypted_ext = header[68 + AES_BLOCK_SIZE :]
        dest_ext = str(_unpad_bytes(decryptor.update(encrypted_ext)), "utf-8")
        dest_ext = dest_ext if dest_ext == "" else "." + dest_ext

        dest = src.with_suffix(dest_ext)
        with open(dest, "wb") as dest_:
            for chunk in iter(partial(src_.read, buffer_size), b""):
                chunk_len = len(chunk)
                chunk = decryptor.update(chunk)
                chunk = _unpad_bytes(chunk)
                dest_.write(chunk)
                yield chunk_len
            dest_.write(decryptor.finalize())


def _unpad_bytes(bytes_in: bytes) -> bytes:
    unpadder = padding.PKCS7(AES_BLOCK_SIZE * 8).unpadder()
    try:
        unpadded: bytes = unpadder.update(bytes_in) + unpadder.finalize()
        return unpadded
    except ValueError:
        return bytes_in
