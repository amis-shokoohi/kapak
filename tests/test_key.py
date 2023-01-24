import base64

from kapak.key import derive_key


def test_derive_key() -> None:
    password = "P@ssw0rd"
    salt = 16 * b"\x00"
    expected_key = b"ddsmaX1zc8IxVYOTGRbAy2zk+ImlRiub6ZRzgZXc4rU="

    key = derive_key(password, salt)
    assert base64.standard_b64encode(key) == expected_key
