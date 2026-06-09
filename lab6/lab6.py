# Быстрое возведение в степень (Square-and-Multiply)
def hamming_weight(x):
    return bin(x).count("1")

def fast_powering(base, exp, mod):
    if mod == 1:
        return 0, 0
    if exp == 0:
        print("\nРезультат: 1")
        print("Количество умножений: 0")
        return 1, 0
    base = base % mod
    result = base
    counter = 0
    binary_exp = bin(exp)[2:]
    print(f"Основание: {base}")
    print(f"Показатель: {exp}")
    print(f"Двоичная запись: {binary_exp}")
    print(f"Вес Хэмминга: {hamming_weight(exp)}")
    print(f"Модуль: {mod}")
    print(f"{'Шаг':<5}" f"{'Бит':<6}" f"{'Операция':<20}" f"{'Результат':<15}" f"{'Умножений':<12}")
    print(f"{0:<5}" f"{'-':<6}" f"{'Начальное значение':<20}" f"{result:<15}" f"{counter:<12}")
    step = 0
    for bit in binary_exp[1:]:
        step += 1
        result = (result * result) % mod
        counter += 1
        operation = "Квадрат"
        if bit == "1":
            result = (result * base) % mod
            counter += 1
            operation = "Квадрат + умнож."
        print(f"{step:<5}" f"{bit:<6}" f"{operation:<20}" f"{result:<15}" f"{counter:<12}")
    print(f"Результат: {result}")
    print(f"Количество умножений: {counter}")
    return result, counter

def main():
    n = 0
    while n < 3:
        try:
            n += 1
            print("\nВведите: base exp mod")
            base, exp, mod = map(int, input().split())
            result, mults = fast_powering(base, exp, mod)
            print("\nПроверка через встроенный pow():")
            print(f"pow({base}, {exp}, {mod}) = {pow(base, exp, mod)}")
            if result == pow(base, exp, mod):
                print("Проверка пройдена")
            else:
                print("ОШИБКА")
        except KeyboardInterrupt:
            print("\nЗавершение работы")
            break
        except Exception as e:
            print("Ошибка:", e)

if __name__ == "__main__":
    main()

# для демо
def hamming_weight(x):
    return bin(x).count("1")

def fast_powering_count(base, exp, mod):
    if exp == 0:
        return 1, 0
    result = base % mod
    counter = 0
    for bit in bin(exp)[2:][1:]:
        result = (result * result) % mod
        counter += 1
        if bit == "1":
            result = (result * base) % mod
            counter += 1
    return result, counter

def demo_hamming():
    base = 5
    mod = 23
    exponents = [
        8,    # 1000 вес=1
        9,    # 1001 вес=2
        15,   # 1111 вес=4
        31    # 11111 вес=5
    ]
    print("ЗАВИСИМОСТЬ КОЛИЧЕСТВА УМНОЖЕНИЙ ОТ ВЕСА ХЭММИНГА")
    print(f"{'Степень':<10}" f"{'Двоичная':<12}" f"{'Вес':<10}" f"{'Умножений':<15}")
    for exp in exponents:
        _, mults = fast_powering_count(base, exp, mod)
        print(f"{exp:<10}" f"{bin(exp)[2:]:<12}" f"{hamming_weight(exp):<10}" f"{mults:<15}")

demo_hamming()
