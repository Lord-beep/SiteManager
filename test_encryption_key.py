from paths import CONFIG_DIR
from security.encryption import (
    EncryptionManager,
    load_or_create_key
)


KEY_PATH = CONFIG_DIR / "encryption.key"


key = load_or_create_key(KEY_PATH)

encryption = EncryptionManager(key)

original = "API_KEY_TESTE_123456"

encrypted = encryption.encrypt(original)

decrypted = encryption.decrypt(encrypted)


print("Chave localizada em:")
print(KEY_PATH)

print("\nOriginal:")
print(original)

print("\nDesencriptado:")
print(decrypted)

print("\nTeste:")

if original == decrypted:
    print("OK - chave persistente funciona!")
else:
    print("ERRO!")
