import hashlib
import secrets
import math

# использовала SHA-256, но только часть хеша, чтобы увеличить вероятность коллизии
# для 16-битного хеша N = 2^16 = 65536 коллизия появляется примерно после √65536 = 256 случ. сообщений

# Парадокс дней рождения
# В группе всего 23 человека, вероятность совпадения дней рождения больше 50%, хотя возможных дат 365


# SHA-256 с усечением до заданного числа бит
def hash_truncated(data: bytes, bits: int) -> int:
    digest = hashlib.sha256(data).digest()
    hash_int = int.from_bytes(digest, "big")
    return hash_int >> (256 - bits)

# случайное сообщение
def random_message(length=16):
    return secrets.token_bytes(length)

# поиск коллизии
def birthday_attack(bits=16):
    seen = {}
    attempts = 0
    while True:
        attempts += 1
        message = random_message()
        h = hash_truncated(message, bits)
        if h in seen:
            return (seen[h], message, h, attempts)
        seen[h] = message

def preimage_attack(target_hash, bits=16):
    attempts = 0
    while True:
        attempts += 1
        candidate = random_message()
        h = hash_truncated(candidate, bits)
        if h == target_hash:
            return candidate, attempts
