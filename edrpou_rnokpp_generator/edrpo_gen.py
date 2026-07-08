import random
from pathlib import Path


def calc_control_for_7digits(digits7: list[int]) -> int:
    """Розрахунок контрольного розряду для 7-значного базового коду."""
    if len(digits7) != 7 or any(not (0 <= d <= 9) for d in digits7):
        raise ValueError("digits7 must be a list of 7 integers in 0..9")

    int_value = int("".join(map(str, digits7)))

    # Вибір базового та альтернативного наборів ваг
    if 3_000_000 <= int_value <= 6_000_000:
        weights_base = [7, 1, 2, 3, 4, 5, 6]
        weights_alt = [9, 3, 4, 5, 6, 7, 8]
    else:
        weights_base = [1, 2, 3, 4, 5, 6, 7]
        weights_alt = [3, 4, 5, 6, 7, 8, 9]

    def mod11(w: list[int]) -> int:
        return sum(d * wi for d, wi in zip(digits7, w)) % 11

    # Перша спроба
    r = mod11(weights_base)
    if r < 10:
        return r

    # Альтернативна спроба (якщо залишок був 10)
    r = mod11(weights_alt)
    return r if r < 10 else 0


def generate_edrpou(prefix: str = "35") -> str:
    """Згенерувати валідний код ЄДРПОУ (8 цифр)."""
    if not isinstance(prefix, str) or len(prefix) != 2 or not prefix.isdigit():
        raise ValueError("prefix must be a 2-digit string, e.g. '46'")

    digits = [int(ch) for ch in prefix] + [random.randint(0, 9) for _ in range(5)]
    control = calc_control_for_7digits(digits)

    return "".join(map(str, digits)) + str(control)


def validate_edrpou(code: str) -> bool:
    """Перевіряє коректність коду ЄДРПОУ. Повертає True/False."""
    if not isinstance(code, str) or len(code) != 8 or not code.isdigit():
        return False

    digits7 = [int(ch) for ch in code[:7]]
    actual_control = int(code[7])
    expected_control = calc_control_for_7digits(digits7)

    return actual_control == expected_control


def generate_edrpou_list(prefix: str = "35", count: int = 40) -> list[str]:
    """Генерує список ЄДРПОУ та зберігає їх у файл."""
    edrpou_list = [generate_edrpou(prefix) for _ in range(count)]

    output_dir = Path("generated")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "generated_edrpo.txt"
    with output_file.open("w", encoding="utf-8") as f:
        f.write("\n".join(edrpou_list) + "\n")

    return edrpou_list
