import random
import os
from datetime import datetime
import sys
#генерація іпна
def generate_ipn(date_str:str)->str:
    #парсонс дати
    def parse_date(date_str: str):
        formats = ["%d.%m.%Y", "%d,%m,%Y", "%d-%m-%Y", "%d/%m/%Y", "%d%m%Y", "%d %m %Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError("Невірний формат дати! Використовуйте ДД.ММ.РРРР або інший підтримуваний формат.")

    birth_date = parse_date(date_str)

    #кількість днів від 01.01.1900from
    base_date = datetime(1900,1,1)
    days = (birth_date - base_date).days + 1
    if days < 0:
        raise ValueError('Date can\'t be less than 01.01.1900')

    #перші 5 цифр = к-сть днів
    days_part = f"{days:05d}"

    #наступні 4 цифри - випадкові
    serial_part = f"{random.randint(0,9999):04d}"

    #перші 9 в рядку
    first_nain = days_part + serial_part

    #контрольна цифра
    weights = [10,9,8,7,6,5,4,3,2]
    total = sum(int(first_nain[i]) * weights[i] for i in range(9))
    control = (total % 11) % 10

    return first_nain + str(control)

def generate_ipn_list(date_str: str, count: int = 40):
    ipn_list = [generate_ipn(date_str) for _ in range(count)]
    with open("generated/generated_ipns.txt", "w") as f:
        for ipn in ipn_list:
            f.write(ipn + "\n")
    return ipn_list

# додати автоматичну вибір дати
# перевірку чи є даний іпн в базі