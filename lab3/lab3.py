import secrets
from pathlib import Path

# Генерация ключей
def generate_key_secrets(filename, size):
    with open(filename, "wb") as file:
        file.write(secrets.token_bytes(size))

# Шифр вернама
def vernam_cipher(input_file, key_file, output_file):
    with open(input_file, "rb") as file:
        data = file.read()
    with open(key_file, "rb") as file:
        key = file.read()
    if len(key) < len(data):
        raise ValueError("Длина ключа должна быть не меньше длины сообщения")
    result = bytes(byte ^ key_byte for byte, key_byte in zip(data, key))
    with open(output_file, "wb") as file:
        file.write(result)

# RC4
def rc4_keystream(key):
    S = list(range(256))
    j = 0
    # KSA
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = 0
    j = 0
    # PRGA
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def rc4_process(input_file, output_file, key):
    with open(input_file, "rb") as file:
        data = file.read()
    stream = rc4_keystream(key)
    result = bytes(byte ^ next(stream) for byte in data)
    with open(output_file, "wb") as file:
        file.write(result)

# Вспомогательные функции
def files_are_equal(file1, file2):
    with open(file1, "rb") as f1:
        data1 = f1.read()
    with open(file2, "rb") as f2:
        data2 = f2.read()
    return data1 == data2

def file_size(filename):
    return Path(filename).stat().st_size

text = ("Vernam cipher and RC4 stream cipher demonstration.\n" * 100)
with open("plaintext.txt", "w", encoding="utf-8") as file:
    file.write(text)
plaintext_size = file_size("plaintext.txt")