import math
import random
from collections import Counter

random.seed(42)

# Подсчёт частот байтов.
def count_frequencies(filename):
    with open(filename, "rb") as file:
        data = file.read()
    frequencies = Counter(data)
    return frequencies, len(data)

# Вычисление энтропии Шеннона.
def calculate_entropy(frequencies, total_symbols):
    entropy = 0.0
    if total_symbols == 0:
      return entropy
    for count in frequencies.values():
        probability = count / total_symbols
        entropy -= probability * math.log2(probability)
    return entropy

# нужна для генерации файла с английскими словами
def generate_text_file(size):
    text = ("HELLO WORLD THIS IS AN EXAMPLE OF INFORMATION ENTROPY " * ((size // 55) + 1))
    return text[:size].encode("ascii")

# Создание файлов для экспериментов
def generate_test_files():
    size = 100000
    # 1. Одинаковые символы
    with open("same_symbols.bin", "wb") as file:
        file.write(b"A" * size)
    # 2. Случайные 0 и 1
    with open("random_binary.bin", "wb") as file:
        data = bytes(random.choice(b"01") for _ in range(size))
        file.write(data)
    # 3. Случайные байты 0..255
    with open("random_bytes.bin", "wb") as file:
        data = bytes(random.randint(0, 255) for _ in range(size))
        file.write(data)
    # 4. Файл с английским текстом
    with open("english_text.txt", "wb") as file:
        file.write(generate_text_file(size))
    print("Тестовые файлы созданы.")

# теоретическое значение энтропии
def theoretical_entropy(alphabet_size):
    if alphabet_size <= 1:
        return 0.0
    return math.log2(alphabet_size)

def main():
    generate_test_files()
    files = [("same_symbols.bin", 1), ("random_binary.bin", 2), ("random_bytes.bin", 256)]
    print("\nРезультаты:")
    for filename, alphabet_size in files:
        frequencies, total = count_frequencies(filename)
        entropy = calculate_entropy(frequencies, total)
        theoretical = theoretical_entropy(alphabet_size)
        print(f"\nФайл: {filename}")
        print(f"Размер: {total} байт")
        print(f"Количество различных байтов: {len(frequencies)}")
        print(f"Практическая энтропия: {entropy:.6f}")
        print(f"Теоретическая энтропия: " f"{theoretical:.6f}")
        print(f"Отклонение: " f"{abs(entropy - theoretical):.6f}")
    filename = "english_text.txt"
    frequencies, total = count_frequencies(filename)
    entropy = calculate_entropy(frequencies, total)
    print(f"\nФайл: {filename}")
    print(f"Размер: {total} байт")
    print(f"Практическая энтропия: {entropy:.6f}")

if __name__ == "__main__":
    main()