from kapak.key import derive_key


def test_derive_key() -> None:
    password = "P@ssw0rd"
    salt = 16 * b"\x00"
    expected_key = "75db26697d7373c2315583931916c0cb6ce4f889a5462b9be994738195dce2b5"

    key = derive_key(password, salt)
    assert key.hex() == expected_key
