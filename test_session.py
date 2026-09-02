from pathlib import Path

from security.session import SecuritySession


KEY_PATH = Path("config/encryption.key")

PASSWORD = "MinhaPasswordMestre123!"


session = SecuritySession(
    PASSWORD,
    KEY_PATH
)


print("A desbloquear sessão...")

if session.unlock():

    print("OK - sessão desbloqueada!")

    encrypted = session.encryption.encrypt(
        "DADO_SECRETO"
    )

    print("\nDados encriptados:")
    print(encrypted)

    decrypted = session.encryption.decrypt(
        encrypted
    )

    print("\nDados desencriptados:")
    print(decrypted)

else:

    print("ERRO - não foi possível desbloquear!")


print("\nA bloquear sessão...")

session.lock()

try:

    session.encryption.encrypt(
        "TESTE"
    )

    print("ERRO - sessão ainda está desbloqueada!")

except RuntimeError:

    print("OK - sessão bloqueada!")
