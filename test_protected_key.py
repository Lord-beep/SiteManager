from pathlib import Path

from cryptography.fernet import InvalidToken

from security.encryption import (
    create_protected_key,
    load_protected_key
)


KEY_PATH = Path("config/encryption.key")

PASSWORD = "MinhaPasswordMestre123!"
WRONG_PASSWORD = "PasswordErrada123!"


print("A criar chave protegida...")

create_protected_key(
    PASSWORD,
    KEY_PATH
)

print("Chave criada!")

print("\nA carregar com password correta...")

key = load_protected_key(
    PASSWORD,
    KEY_PATH
)

print("Chave carregada com sucesso!")

print("\nA testar password errada...")

try:

    load_protected_key(
        WRONG_PASSWORD,
        KEY_PATH
    )

    print("ERRO - a password errada conseguiu desbloquear a chave!")

except InvalidToken:

    print("OK - password errada foi rejeitada!")
