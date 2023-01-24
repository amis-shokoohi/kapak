import base64
from io import BytesIO
from dataclasses import dataclass

import pytest

import kapak.aes
from kapak.error import KapakError
from kapak.version import __version__


@dataclass(frozen=True)
class Data:
    input: bytes
    expect: bytes
    password: str
    buffer_size: int


data_to_encrypt = [
    Data(
        input=b"yFwMtWN+oqXlKi",  # 14 bytes
        expect=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAAChQeWV8Cchmg0sArLzwsek",
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"ElOTSoqLIEg7KygP",  # 16 bytes
        expect=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAADeG+Vf6g5fyEYP7CeyNlbW",
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"vglB8G4IyL31vnt84A0V78+OkOPOu7",  # 30 bytes
        expect=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAABzCQc7gH7WaZ2W+hoFxwyiF8MbLFwsWQHTztNO4MIzPw==",
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"BveQQwKR3TLa5KWOu4TiWLQIJ9gtYlvf",  # 32 bytes
        expect=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAACPw+PuANmeBRSud+pC5FGCEujOIeKeiO/znxeAbKWcDA==",
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"qTMHczZptvZHAsPCIeYXp03v+K1x76Qvv4",  # 34 bytes
        expect=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAABhjOJCTYcelV0wB7kxhHU/cPPjHodUuf+cLf+h9fNWuRmASKQRbuAVm7wu6Xxn3T8=",
        password="P@ssw0rd",
        buffer_size=16,
    ),
]


@pytest.mark.parametrize("data", data_to_encrypt)
def test_encrypt(monkeypatch: pytest.MonkeyPatch, data: Data) -> None:
    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    encrypted_data = b""
    with BytesIO(data.input) as src, BytesIO() as dst:
        for _ in kapak.aes.encrypt(src, dst, data.password, data.buffer_size):
            pass
        encrypted_data = dst.getvalue()

    # Check header
    header_length = int.from_bytes(encrypted_data[:4], "big")
    header = kapak.aes.Header(encrypted_data[4 : 4 + header_length])

    assert header.read(5) == b"kapak"

    srcmajor_version = int.from_bytes(header.read(4), "big")
    assert srcmajor_version == int(__version__.split(".")[0])

    iv = header.read(kapak.aes.AES_BLOCK_SIZE)
    assert iv == kapak.aes.AES_BLOCK_SIZE * b"\x00"

    salt_size = int.from_bytes(header.read(4), "big")
    salt = header.read(salt_size)
    assert salt == salt_size * b"\x00"

    verifier_size = int.from_bytes(header.read(4), "big")
    _ = header.read(verifier_size)
    verifier_hash_size = int.from_bytes(header.read(4), "big")
    _ = header.read(verifier_hash_size)

    reserved_size = int.from_bytes(header.read(4), "big")
    assert reserved_size == 0

    reserved_size = int.from_bytes(header.read(4), "big")
    assert reserved_size == 0

    encrypted_data_length = len(encrypted_data[4 + header_length :])
    assert encrypted_data_length % kapak.aes.AES_BLOCK_SIZE == 0

    assert base64.standard_b64encode(encrypted_data) == data.expect


data_to_decrypt = [
    Data(
        input=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAAChQeWV8Cchmg0sArLzwsek",
        expect=b"yFwMtWN+oqXlKi",  # 14 bytes
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAADeG+Vf6g5fyEYP7CeyNlbW",
        expect=b"ElOTSoqLIEg7KygP",  # 16 bytes
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAABzCQc7gH7WaZ2W+hoFxwyiF8MbLFwsWQHTztNO4MIzPw==",
        expect=b"vglB8G4IyL31vnt84A0V78+OkOPOu7",  # 30 bytes
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAACPw+PuANmeBRSud+pC5FGCEujOIeKeiO/znxeAbKWcDA==",
        expect=b"BveQQwKR3TLa5KWOu4TiWLQIJ9gtYlvf",  # 32 bytes
        password="P@ssw0rd",
        buffer_size=16,
    ),
    Data(
        input=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAABhjOJCTYcelV0wB7kxhHU/cPPjHodUuf+cLf+h9fNWuRmASKQRbuAVm7wu6Xxn3T8=",
        expect=b"qTMHczZptvZHAsPCIeYXp03v+K1x76Qvv4",  # 34 bytes
        password="P@ssw0rd",
        buffer_size=16,
    ),
]


@pytest.mark.parametrize("data", data_to_decrypt)
def test_decrypt(monkeypatch: pytest.MonkeyPatch, data: Data) -> None:
    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    decrypted_data = b""
    with BytesIO(base64.standard_b64decode(data.input)) as src, BytesIO() as dst:
        for _ in kapak.aes.decrypt(src, dst, data.password, data.buffer_size):
            pass
        decrypted_data = dst.getvalue()

    assert decrypted_data == data.expect


def test_decrypt_wrong_password(monkeypatch: pytest.MonkeyPatch) -> None:
    data = Data(
        input=b"AAAAbWthcGFrAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAAChQeWV8Cchmg0sArLzwsek",
        expect=b"yFwMtWN+oqXlKi",  # 14 bytes
        password="Wr0ngP@ssw0rd",
        buffer_size=16,
    )

    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    with BytesIO(base64.standard_b64decode(data.input)) as src, BytesIO() as dst:
        with pytest.raises(KapakError, match=r"wrong password"):
            for _ in kapak.aes.decrypt(src, dst, data.password, data.buffer_size):
                pass


def test_decrypt_unmatching_version(monkeypatch: pytest.MonkeyPatch) -> None:
    data = Data(
        input=b"AAAAbWthcGFrAAAnDwAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABBOIB2Sf1bxlU6Lv8t8bRZIAAAAIGDHZk3R4+1yU9A/844W8c3N6Jh491AISA2ZpmQBHISUAAAAAAAAAAChQeWV8Cchmg0sArLzwsek",
        expect=b"yFwMtWN+oqXlKi",  # 14 bytes
        password="P@ssw0rd",
        buffer_size=16,
    )

    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    with BytesIO(base64.standard_b64decode(data.input)) as src, BytesIO() as dst:
        with pytest.raises(
            KapakError,
            match=r"source version does not match the current version of Kapak",
        ):
            for _ in kapak.aes.decrypt(src, dst, data.password, data.buffer_size):
                pass


def test_decrypt_random_data(monkeypatch: pytest.MonkeyPatch) -> None:
    data = Data(
        input=b"cmFuZG9tIGRhdGE=",
        expect=b"",
        password="",
        buffer_size=0,
    )

    monkeypatch.setattr(kapak.aes, "urandom", lambda n: n * b"\x00")

    with BytesIO(base64.standard_b64decode(data.input)) as src, BytesIO() as dst:
        with pytest.raises(KapakError, match=r"not able to decrypt this file format"):
            for _ in kapak.aes.decrypt(src, dst, data.password):
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
