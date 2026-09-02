from security import encrypt_data, decrypt_data


password = "MinhaPasswordMestre123!"

salt = b"1234567890123456"

secret = "API_KEY_SUPER_SECRETA_123"


print("Dados originais:")
print(secret)

encrypted = encrypt_data(secret, password, salt)

print("\nDados encriptados:")
print(encrypted)

decrypted = decrypt_data(encrypted, password, salt)

print("\nDados desencriptados:")
print(decrypted)
