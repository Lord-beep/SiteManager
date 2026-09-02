from pathlib import Path

from database import (
    initialize_database,
    add_site,
    get_credentials,
)

from security.security_manager import SecurityManager

from paths import (
    MASTER_PASSWORD_PATH,
    ENCRYPTION_KEY_PATH,
)


PASSWORD = "MinhaPasswordMestre123!"


print("A inicializar base de dados...")

initialize_database()

print("Base de dados inicializada!")


print("\nA preparar segurança...")

security = SecurityManager(
    MASTER_PASSWORD_PATH,
    ENCRYPTION_KEY_PATH
)


if not security.has_master_password():

    security.setup(PASSWORD)

    print("Password mestre criada!")

else:

    print("Password mestre já existe!")


if not security.unlock(PASSWORD):

    raise RuntimeError(
        "Não foi possível desbloquear a segurança."
    )


print("Segurança desbloqueada!")


print("\nA adicionar site de teste...")

site_id = add_site(
    name="Site Seguro",
    platform="PythonAnywhere",
    interval_minutes=60,
    username="utilizador_teste",
    password="password_falsa",
    api_key="API_KEY_TESTE_123456",
    encryption=security.encryption,
)

print(
    f"Site criado com ID: {site_id}"
)


print("\nA recuperar credenciais...")

credentials = get_credentials(
    site_id,
    security.encryption,
)


print("Username:", credentials["username"])
print("Password:", credentials["password"])
print("API Key:", credentials["api_key"])


print("\nA verificar dados...")

if credentials["username"] == "utilizador_teste":
    print("OK - username correto!")
else:
    print("ERRO - username incorreto!")


if credentials["password"] == "password_falsa":
    print("OK - password correta!")
else:
    print("ERRO - password incorreta!")


if credentials["api_key"] == "API_KEY_TESTE_123456":
    print("OK - API Key correta!")
else:
    print("ERRO - API Key incorreta!")


security.lock()

print("\nSegurança bloqueada.")
print("Teste terminado!")
