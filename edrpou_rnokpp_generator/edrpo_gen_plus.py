import random
import sys
from datetime import datetime

#def edrpo_gen(date_str:str)->str:
#    pass
#import random


def calc_control_for_7digits(digits7):
    """
    Розрахунок контрольного розряду для 7-значного базового коду (без контрольної цифри).

    Алгоритм (реалізовано згідно з публічними методичними описами):
    1) Визначити числову величину 7-значного коду (наприклад, [4,1,5,6,4,4,5] -> 4156445).
    2) Якщо ця величина лежить у межах [3_000_000; 6_000_000], використовуються ваги
       [7, 1, 2, 3, 4, 5, 6] (цикл зсунутий на одну позицію). Інакше — ваги [1,2,3,4,5,6,7].
    3) Обчислити S = sum(d_i * w_i) і r = S % 11.
       - Якщо r != 10 → контрольна = r.
       - Якщо r == 10 → пробуємо альтернативні послідовності ваг: [3,4,5,6,7,8,9] та [9,3,4,5,6,7,8].
       - Якщо після альтернативних спроб r == 10 → контрольна = 0.

    Примітка: ця логіка відповідає опису, наведеному у навчально-методичному матеріалі.
    """

    if len(digits7) != 7 or any((not isinstance(d, int) or d < 0 or d > 9) for d in digits7):
        raise ValueError("digits7 must be a list of 7 integers in 0..9")

    int_value = int("".join(map(str, digits7)))

    # Вибір базового набору ваг залежно від числового інтервалу
    if 3_000_000 <= int_value <= 6_000_000:
        weights = [7, 1, 2, 3, 4, 5, 6]
    else:
        weights = [1, 2, 3, 4, 5, 6, 7]

    def mod11(d, w):
        s = sum(di * wi for di, wi in zip(d, w))
        return s % 11

    r = mod11(digits7, weights)
    if r != 10:
        return r

    # Якщо залишок 10 — пробуємо альтернативні набори ваг
    for alt in ([3, 4, 5, 6, 7, 8, 9], [9, 3, 4, 5, 6, 7, 8]):
        r = mod11(digits7, alt)
        if r != 10:
            return r

    # Якщо і після альтернативи отримали 10 — ставимо 0
    return 0


def generate_edrpou(prefix="35"):
    """
    Згенерувати валідний (форматно) код ЄДРПОУ (8 цифр).

    - prefix: двозначний префікс, наприклад "46" (за бажанням можна передати інший).
    - Повертає рядок з 8 цифр.

    Логіка: фіксований префікс (2 цифри) + 5 випадкових цифр → отримуємо 7 цифр → обчислюємо
    контрольний розряд функцією calc_control_for_7digits і додаємо як 8-му цифру.
    """

    if not isinstance(prefix, str) or len(prefix) != 2 or not prefix.isdigit():
        raise ValueError("prefix must be a 2-digit string, e.g. '46'")

    digits = [int(ch) for ch in prefix]
    digits += [random.randint(0, 9) for _ in range(5)]  # отримуємо 7 цифр

    control = calc_control_for_7digits(digits)
    digits.append(control)

    return "".join(map(str, digits))


def validate_edrpou(code):
    """
    Перевіряє коректність (формальну) коду ЄДРПОУ.
    Повертає (is_valid: bool, expected_control: int).
    """
    if not isinstance(code, str) or len(code) != 8 or not code.isdigit():
        raise ValueError("code must be an 8-digit string")

    digits7 = [int(ch) for ch in code[:7]]
    actual_control = int(code[7])
    expected_control = calc_control_for_7digits(digits7)
    return actual_control == expected_control, expected_control

def generato_self_validator():
    with open('generated/generated_edrpo.txt', 'w') as f:
        # Декілька згенерованих прикладів
        for _ in range(200):
            code = generate_edrpou(prefix="35")
            f.write(code+'\n')
            ok, expected = validate_edrpou(code)
            print(f"Код {code}: валідний={ok}, очікувана контрольна={expected}")

if __name__ == "__main__":
    generato_self_validator()