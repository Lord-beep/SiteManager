from pathlib import Path

from security.security_manager import SecurityManager


PASSWORD_FILE = Path(
    "config/test_manager_password.dat"
)

KEY_FILE = Path(
    "config/test_manager.key"
)

PASSWORD = "MinhaPasswordMestre123!"
WRONG_PASSWORD = "PasswordErrada123!"


# Limpar testes anteriores

for file in [PASSWORD_FILE, KEY_FILE]:

    if file.exists():
        file.unlink()


security = SecurityManager(
    PASSWORD_FILE,
    KEY_FILE
)


print("1. Password configurada?")

print(
    security.has_master_password()
)


print("\n2. A configurar...")

security.setup(
    PASSWORD
)

print("OK - configuração criada!")


print("\n3. A testar password errada...")

if not security.unlock(WRONG_PASSWORD):

    print("OK - password errada rejeitada!")

else:

    print("ERRO!")


print("\n4. A desbloquear...")

if security.unlock(PASSWORD):

    print("OK - aplicação desbloqueada!")

else:

    print("ERRO - não desbloqueou!")

    raise SystemExit


print("\n5. A testar encriptação...")

encrypted = security.encryption.encrypt(
    "DADO_SUPER_SECRETO"
)

decrypted = security.encryption.decrypt(
    encrypted
)

print("Desencriptado:", decrypted)


if decrypted == "DADO_SUPER_SECRETO":

    print("OK - encriptação funciona!")

else:

    print("ERRO!")


print("\n6. A bloquear...")

security.lock()

try:

    security.encryption.encrypt(
        "TESTE"
    )

    print("ERRO - aplicação continua desbloqueada!")

except RuntimeError:

    print("OK - aplicação bloqueada!")
