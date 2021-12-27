from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend


def derive_key(password: str, salt: bytes) -> bytes:
    password_ = bytes(password, "utf-8")
    # Requires 256MB of RAM
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=1 << 18,  # number of iterations
        r=8,  # block size
        p=1,  # number of threads
        backend=default_backend(),
    )
    key = kdf.derive(password_)
    return key
