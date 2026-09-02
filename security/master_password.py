import base64
import hashlib
import hmac
import os
from pathlib import Path


SALT_SIZE = 16
PBKDF2_ITERATIONS = 600_000


class MasterPasswordManager:

    def __init__(self, password_file: Path):
        self.password_file = password_file

    def has_password(self) -> bool:
        return self.password_file.exists()

    def setup_password(self, password: str) -> None:

        if self.has_password():
            raise RuntimeError(
                "A password mestre já foi configurada."
            )

        if len(password) < 8:
            raise ValueError(
                "A password deve ter pelo menos 8 caracteres."
            )

        salt = os.urandom(SALT_SIZE)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS
        )

        self.password_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.password_file.open("wb") as file:
            file.write(salt)
            file.write(password_hash)

    def verify_password(self, password: str) -> bool:

        if not self.has_password():
            return False

        with self.password_file.open("rb") as file:

            salt = file.read(SALT_SIZE)
            stored_hash = file.read()

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS
        )

        return hmac.compare_digest(
            password_hash,
            stored_hash
        )

    def change_password(
        self,
        current_password: str,
        new_password: str
    ) -> None:

        if not self.verify_password(current_password):
            raise ValueError(
                "A password atual está incorreta."
            )

        if len(new_password) < 8:
            raise ValueError(
                "A nova password deve ter pelo menos 8 caracteres."
            )

        salt = os.urandom(SALT_SIZE)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            new_password.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS
        )

        with self.password_file.open("wb") as file:

            file.write(salt)
            file.write(password_hash)