import string

ALPHABET = string.ascii_uppercase

# пример словаря
ENGLISH_DICTIONARY = {
    "THE", "BE", "TO", "OF", "AND", "A", "IN", "THAT",
    "HAVE", "I", "IT", "FOR", "NOT", "ON", "WITH",
    "HE", "AS", "YOU", "DO", "AT", "THIS", "BUT",
    "HIS", "BY", "FROM", "HELLO", "WORLD", "IS",
    "ARE", "WE", "THEY", "SECRET", "MESSAGE",
    "CRYPTOGRAPHY", "ATTACK", "CAESAR"
}

# сдвиг буквы
def shift_character(char, key):
    if char not in ALPHABET:
        return char
    index = ALPHABET.index(char)
    new_index = (index + key) % 26
    return ALPHABET[new_index]

# шифрование текста
def caesar_encrypt(text, key):
    text = text.upper()
    result = ""
    for char in text:
        result += shift_character(char, key)
    return result

# расшифрование текста
def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

# определение ключа по открытому и шифрованному тексту
# для простоты возвращается первый найденный ключ
def find_key_known_plaintext(plaintext, ciphertext):
    plaintext = plaintext.upper()
    ciphertext = ciphertext.upper()
    for p_char, c_char in zip(plaintext, ciphertext):
        if p_char in ALPHABET and c_char in ALPHABET:
            p_index = ALPHABET.index(p_char)
            c_index = ALPHABET.index(c_char)
            key = (c_index - p_index) % 26
            return key
    raise ValueError("No alphabetic characters found.")

# вывод всех вариантов расшифрования
def bruteforce_attack(ciphertext):
    variants = {}
    for key in range(26):
        variants[key] = caesar_decrypt(ciphertext, key)
    return variants

# подсчет найденных в словаре слов: чем  больше, тем лучше
def score_text(text):
    words = text.upper().split()
    score = 0
    for word in words:
        cleaned = ''.join(ch for ch in word if ch.isalpha())
        if cleaned in ENGLISH_DICTIONARY:
            score += 1
    return score

# автоматический подбор ключа
def automatic_dictionary_attack(ciphertext):
    best_key = None
    best_text = None
    best_score = -1
    for key in range(26):
        candidate = caesar_decrypt(ciphertext, key)
        score = score_text(candidate)
        if score > best_score:
            best_score = score
            best_key = key
            best_text = candidate
    return best_key, best_text