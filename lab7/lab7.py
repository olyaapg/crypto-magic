import math

# Быстрое возведение в степень
def fast_power(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

# Обратный элемент по модулю
def modinv(a, p):
    old_r, r = a, p
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if old_r != 1:
        raise ValueError("Обратный элемент не существует")
    return old_s % p

# Полный перебор
def bruteforce_dlog(g, h, p):
    print("МЕТОД ПОЛНОГО ПЕРЕБОРА")
    current = 1
    mults = 0
    print(f"{'x':<10}{'g^x mod p':<15}")
    for x in range(p - 1):
        print(f"{x:<10}{current:<15}")
        if current == h:
            print("\nРешение найдено")
            print(f"x = {x}")
            return x, mults
        current = (current * g) % p
        mults += 1
    return None, mults

# Метод Шэнкса
def shanks_dlog(g, h, p):
    print("МЕТОД ШЭНКСА (BABY STEP - GIANT STEP)")
    n = p - 1
    m = math.ceil(math.sqrt(n))
    k = math.ceil(n / m)
    print(f"\nn = {n}")
    print(f"m = {m}")
    print(f"k = {k}")
    mults = 0
    baby = {}
    print("\nШАГ МЛАДЕНЦА")
    print(f"{'j':<10}{'g^j mod p':<15}")
    current = 1
    for j in range(m):
        baby[current] = j
        print(f"{j:<10}{current:<15}")
        current = (current * g) % p
        mults += 1
    gm = fast_power(g, m, p)
    factor = modinv(gm, p)
    print(f"\ng^m mod p = {gm}")
    print(f"(g^m)^(-1) mod p = {factor}")
    print("\nШАГ ВЕЛИКАНА")
    print(f"{'i':<10}{'value':<15}")
    current = h
    for i in range(k):
        print(f"{i:<10}{current:<15}")
        if current in baby:
            j = baby[current]
            x = i * m + j
            print("\nСовпадение найдено!")
            print(f"i = {i}")
            print(f"j = {j}")
            print(f"x = i*m + j")
            print(f"x = {i}*{m} + {j}")
            print(f"x = {x}")
            return x, mults
        current = (current * factor) % p
        mults += 1
    return None, mults

# Один тест
def run_test(p, g, x_real):
    h = fast_power(g, x_real, p)
    print(f"p = {p}")
    print(f"g = {g}")
    print(f"x = {x_real}")
    print(f"h = g^x mod p = {h}")
    x1, brute_mults = bruteforce_dlog(g, h, p)
    print(f"\nКоличество умножений: {brute_mults}")
    x2, shanks_mults = shanks_dlog(g, h, p)
    print(f"\nКоличество умножений: {shanks_mults}")
    print("ПРОВЕРКА")
    print(f"Полный перебор : x = {x1}")
    print(f"Шэнкс          : x = {x2}")
    print("\nСРАВНЕНИЕ")
    print(f"Полный перебор : {brute_mults} умножений")
    print(f"Шэнкс          : {shanks_mults} умножений")
    if shanks_mults > 0:
        print(f"Ускорение      : " f"{brute_mults / shanks_mults:.2f} раза")
