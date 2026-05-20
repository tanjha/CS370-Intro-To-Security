import numpy as np
import timeit

max = 60


def int_to_key1(n):
    key = np.base_repr(n, base=26).zfill(6)
    standard = "0123456789ABCDEFGHIJKLMNOP"
    conv = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    translation_table = str.maketrans(standard, conv)
    key = key.translate(translation_table)

    return key[::-1]


def int_to_key2(n):
    chars = []
    for _ in range(6):
        chars.append(n % 26)
        n //= 26
    return bytes(c + 65 for c in chars)


def int_to_key3(n):
    n, a = divmod(n, 26)
    n, b = divmod(n, 26)
    n, c = divmod(n, 26)
    n, d = divmod(n, 26)
    n, e = divmod(n, 26)
    return bytes([a + 65, b + 65, c + 65, d + 65, e + 65, n % 26 + 65])


time_a = timeit.timeit(lambda: int_to_key1(60), number=10000)
time_b = timeit.timeit(lambda: int_to_key2(60), number=10000)
time_c = timeit.timeit(lambda: int_to_key3(60), number=10000)


print(f"Method A: {time_a:.4f}s")
print(f"Method B: {time_b:.4f}s")
print(f"Method C: {time_c:.4f}s")
