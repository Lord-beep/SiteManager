import base64
import hashlib
import os
from pathlib import Path

from cryptography.fernet import Fernet


PBKDF2_ITERATIONS = 600_000
SALT_SIZE = 16


class EncryptionManager:

    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, value: str) -> bytes:
        return self.fernet.encrypt(
            value.encode("utf-8")
        )

    def decrypt(self, value: bytes) -> str:
        return self.fernet.decrypt(
            value
        ).decode("utf-8")


def derive_key(password: str, salt: bytes) -> bytes:

    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=32
    )

    return base64.urlsafe_b64encode(key)


def create_protected_key(
    password: str,
    key_path: Path
) -> None:

    salt = os.urandom(SALT_SIZE)

    encryption_key = Fernet.generate_key()

    protection_key = derive_key(
        password,
        salt
    )

    fernet = Fernet(protection_key)

    encrypted_key = fernet.encrypt(
        encryption_key
    )

    key_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with key_path.open("wb") as file:

        file.write(salt)
        file.write(encrypted_key)


def load_protected_key(
    password: str,
    key_path: Path
) -> bytes:

    with key_path.open("rb") as file:

        salt = file.read(SALT_SIZE)
        encrypted_key = file.read()

    protection_key = derive_key(
        password,
        salt
    )

    fernet = Fernet(protection_key)

    return fernet.decrypt(
        encrypted_key
    )
