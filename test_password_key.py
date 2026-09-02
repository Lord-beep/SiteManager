import os

from security.encryption import derive_key


password = "MinhaPasswordMestre123!"

salt = os.urandom(16)

key1 = derive_key(password, salt)
key2 = derive_key(password, salt)

print("Salt:")
print(salt.hex())

print("\nChave 1:")
print(key1)

print("\nChave 2:")
print(key2)

print("\nTeste:")

if key1 == key2:
    print("OK - a mesma password produz a mesma chave!")
else:
    print("ERRO - as chaves são diferentes!")
