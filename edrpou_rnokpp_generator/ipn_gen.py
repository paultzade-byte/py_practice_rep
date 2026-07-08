import random
from datetime import datetime
from pathlib import Path
   
# weights
ipn_weights = [-1, 5, 7, 9, 4, 6, 10, 5, 7]


def _get_date(date_str: str) -> datetime:
    """Additional function for dare parsing"""
    formats = ["%d.%m.%Y", "%d,%m,%Y", "%d-%m-%Y", "%d/%m/%Y", "%d%m%Y", "%d %m %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Не вірний формат дати: '{date_str}'. Використовуйте цифри та роздільники.")

def generate_ipn(date_str: str) -> str:
    """Generating the valid IPN based on the birth date"""

    birth_date = _get_date(date_str)
    if isinstance(birth_date, str):
        raise ValueError(birth_date)

    base_date = datetime(1900, 1, 1)

    days = (birth_date - base_date).days + 1
    if days < 0:
        raise ValueError("Date cannot be less than 01.01.1900")

    # calculate the first part of IPN code (first five)
    days_part = f"{days:05d}"
    # calculate the second part of IPN code (second four)
    serial_part = f"{random.randint(0,9999):04d}"
    # concatecate two parts of digits
    first_nine = days_part + serial_part

    # control digit is calculates here
    total = sum(int(digit) * weight for digit, weight in zip(first_nine, ipn_weights))
    control = (total % 11) % 10

    return f"{first_nine}{control}"

def generate_ipn_list(date_str: str, count: int = 40) -> list[str]:
    """Generating list of IPN and saving into file"""
    ipn_list = [generate_ipn(date_str) for _ in range (count)]

    # crete the directory if it doesn't exist yet
    generated_dir = Path("generated")
    generated_dir.mkdir(exist_ok=True)

    # create file and write IPN list there
    result_file = generated_dir / "generated_ipns_list.txt"
    with result_file.open("w", encoding="utf-8") as f:
        f.write("\n".join(ipn_list) + "\n")

    return ipn_list