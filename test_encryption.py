from cryptography.fernet import Fernet

from security.encryption import EncryptionManager


key = Fernet.generate_key()

encryption = EncryptionManager(key)

original = "API_KEY_TESTE_123456"

encrypted = encryption.encrypt(original)

decrypted = encryption.decrypt(encrypted)


print("Original:")
print(original)

print("\nEncriptado:")
print(encrypted)

print("\nDesencriptado:")
print(decrypted)

print("\nTeste:")

if original == decrypted:
    print("OK - encriptação funciona!")
else:
    print("ERRO - os dados não correspondem!")
