import random
from io import BytesIO
from dataclasses import dataclass

import pytest

import kapak.aes
from kapak.error import KapakError
from kapak.version import __version__


@dataclass(frozen=True)
class Data:
    input: bytes
    password: str
    buffer_size: int


def test_encrypt_header(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    encrypted_data = b""
    with BytesIO(b"\x00") as src, BytesIO() as dst:
        for _ in kapak.aes.encrypt(src, dst, "P@ssw0rd"):
            pass
        encrypted_data = dst.getvalue()

    # Check header
    header_length = int.from_bytes(encrypted_data[:4], "big")
    header = kapak.aes.Header(encrypted_data[4 : 4 + header_length])

    assert header.read(5) == b"kapak"

    src_major_version = int.from_bytes(header.read(4), "big")
    assert src_major_version == int(__version__.split(".")[0])

    iv = header.read(kapak.aes.AES_BLOCK_SIZE)
    assert iv == kapak.aes.AES_BLOCK_SIZE * b"\x00"

    salt_size = int.from_bytes(header.read(4), "big")
    salt = header.read(salt_size)
    assert salt == kapak.aes.SALT_SIZE * b"\x00"

    verifier_size = int.from_bytes(header.read(4), "big")
    _ = header.read(verifier_size)
    verifier_hash_size = int.from_bytes(header.read(4), "big")
    _ = header.read(verifier_hash_size)

    reserved_size = int.from_bytes(header.read(4), "big")
    assert reserved_size == 0

    reserved_size = int.from_bytes(header.read(4), "big")
    assert reserved_size == 0


def test_encrypt_decrypt(monkeypatch: pytest.MonkeyPatch) -> None:
    cases = [
        Data(
            input=bytes(random.getrandbits(8) for _ in range(12)),
            password="P@ssw0rd",
            buffer_size=16,
        ),
        Data(
            input=bytes(random.getrandbits(8) for _ in range(16)),
            password="P@ssw0rd",
            buffer_size=16,
        ),
        Data(
            input=bytes(random.getrandbits(8) for _ in range(20)),
            password="P@ssw0rd",
            buffer_size=16,
        ),
        Data(
            input=bytes(random.getrandbits(8) for _ in range(32)),
            password="P@ssw0rd",
            buffer_size=16,
        ),
        Data(
            input=bytes(random.getrandbits(8) for _ in range(34)),
            password="P@ssw0rd",
            buffer_size=16,
        ),
    ]

    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    for c in cases:
        encrypted_data = b""
        with BytesIO(c.input) as src, BytesIO() as dst:
            for _ in kapak.aes.encrypt(src, dst, c.password, c.buffer_size):
                pass
            encrypted_data = dst.getvalue()

        header_length = int.from_bytes(encrypted_data[:4], "big")

        encrypted_data_length = len(encrypted_data[4 + header_length :])
        assert encrypted_data_length % kapak.aes.AES_BLOCK_SIZE == 0
        assert encrypted_data_length >= len(c.input)

        decrypted_data = b""
        with BytesIO(encrypted_data) as src, BytesIO() as dst:
            for _ in kapak.aes.decrypt(src, dst, c.password, c.buffer_size):
                pass
            decrypted_data = dst.getvalue()

        assert decrypted_data == c.input


def test_decrypt_wrong_password(monkeypatch: pytest.MonkeyPatch) -> None:
    data = Data(
        input=bytes(random.getrandbits(8) for _ in range(12)),
        password="P@ssw0rd",
        buffer_size=16,
    )

    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    encrypted_data = b""
    with BytesIO(data.input) as src, BytesIO() as dst:
        for _ in kapak.aes.encrypt(src, dst, data.password, data.buffer_size):
            pass
        encrypted_data = dst.getvalue()

    with BytesIO(encrypted_data) as src, BytesIO() as dst:
        with pytest.raises(KapakError, match=r"wrong password"):
            for _ in kapak.aes.decrypt(src, dst, "Wr0ngP@ssw0rd", data.buffer_size):
                pass


def test_decrypt_unmatching_version(monkeypatch: pytest.MonkeyPatch) -> None:
    data = Data(
        input=bytes(random.getrandbits(8) for _ in range(16)),
        password="P@ssw0rd",
        buffer_size=16,
    )

    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")
    monkeypatch.setattr(kapak.aes, "__version__", "0.0.0")

    encrypted_data = b""
    with BytesIO(data.input) as src, BytesIO() as dst:
        for _ in kapak.aes.encrypt(src, dst, data.password, data.buffer_size):
            pass
        encrypted_data = dst.getvalue()

    monkeypatch.setattr(kapak.aes, "__version__", "1.0.0")

    with BytesIO(encrypted_data) as src, BytesIO() as dst:
        with pytest.raises(
            KapakError,
            match=r"source version does not match the current version of Kapak",
        ):
            for _ in kapak.aes.decrypt(src, dst, data.password, data.buffer_size):
                pass


def test_decrypt_random_data(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    rand_bytes = bytes(random.getrandbits(8) for _ in range(16))
    with BytesIO(rand_bytes) as src, BytesIO() as dst:
        with pytest.raises(KapakError, match=r"not able to decrypt this file format"):
            for _ in kapak.aes.decrypt(src, dst, ""):
                pass


def test_decrypt_wrong_buffer_size() -> None:
    wrong_buffer_size = 1

    with BytesIO() as src, BytesIO() as dst:
        with pytest.raises(
            KapakError,
            match=r"buffer size must be a multiple of aes-block-size \(16 bytes\)",
        ):
            for _ in kapak.aes.encrypt(src, dst, "", wrong_buffer_size):
                pass

        with pytest.raises(
            KapakError,
            match=r"buffer size must be a multiple of aes-block-size \(16 bytes\)",
        ):
            for _ in kapak.aes.decrypt(src, dst, "", wrong_buffer_size):
                pass
