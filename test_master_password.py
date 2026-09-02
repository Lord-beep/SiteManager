from pathlib import Path

from security.master_password import MasterPasswordManager


PASSWORD_FILE = Path(
    "config/test_master_password.dat"
)

PASSWORD = "MinhaPasswordMestre123!"
WRONG_PASSWORD = "PasswordErrada123!"


# Limpar teste anterior
if PASSWORD_FILE.exists():
    PASSWORD_FILE.unlink()


manager = MasterPasswordManager(
    PASSWORD_FILE
)


print("Existe password inicialmente?")
print(manager.has_password())


print("\nA configurar password...")

manager.setup_password(
    PASSWORD
)

print("Password configurada!")


print("\nExiste password agora?")
print(manager.has_password())


print("\nA testar password correta...")

if manager.verify_password(PASSWORD):
    print("OK - password correta!")
else:
    print("ERRO - password correta foi rejeitada!")


print("\nA testar password errada...")

if not manager.verify_password(WRONG_PASSWORD):
    print("OK - password errada foi rejeitada!")
else:
    print("ERRO - password errada foi aceite!")


print("\nA testar segunda configuração...")

try:

    manager.setup_password(
        PASSWORD
    )

    print("ERRO - permitiu configurar novamente!")

except RuntimeError:

    print("OK - segunda configuração foi bloqueada!")

