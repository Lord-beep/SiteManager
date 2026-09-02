import base64
import os

from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet


SALT_SIZE = 16


def generate_salt() -> bytes:
    """
    Gera um salt aleatório.
    """
    return os.urandom(SALT_SIZE)


def create_key(password: str, salt: bytes) -> bytes:
    """
    Cria uma chave Fernet a partir da palavra-passe mestre.
    """

    key = hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        type=Type.ID,
    )

    return base64.urlsafe_b64encode(key)


def encrypt_data(data: str, password: str, salt: bytes) -> bytes:
    """
    Encripta dados usando Fernet.
    """

    key = create_key(password, salt)
    fernet = Fernet(key)

    return fernet.encrypt(data.encode("utf-8"))


def decrypt_data(
    encrypted_data: bytes,
    password: str,
    salt: bytes
) -> str:
    """
    Desencripta dados usando Fernet.
    """

    key = create_key(password, salt)
    fernet = Fernet(key)

    return fernet.decrypt(encrypted_data).decode("utf-8")
