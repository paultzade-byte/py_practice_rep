#1 refresh day1
endpoints = [
    {"path": "/users", "status": 200, "time_ms": 150},
    {"path": "/login", "status": 500, "time_ms": 45},
    {"path": "/data", "status": 200, "time_ms": 350},
    {"path": "/settings", "status": 401, "time_ms": 80}
]
alerts = [path["path"] for path in endpoints if (path["status"] == 500 or path["time_ms"] > 200)]
print(alerts)

#2 refresh day1
processes = [
    {"name": "xorg", "ram_mb": 85},
    {"name": "browser", "ram_mb": 450},
    {"name": "keyd", "ram_mb": 2},
    {"name": "docker", "ram_mb": 512},
    {"name": "htop", "ram_mb": 5}
]
lightweight=[]
heavy=[]
for proc in processes:
    if proc["ram_mb"] <= 100:
        lightweight.append(proc["name"])
    else:
        heavy.append(proc["name"])
print(lightweight)
print(heavy)

#3 refresh day1
needed_switches = 46
pack_size = 10
current_switches = 0
packs_bought = 0
while current_switches < needed_switches:
    packs_bought += 1
    current_switches += pack_size
print(packs_bought)

#4 refresh day1
queries = ["SELECT", "INSERT", "SELECT", "UPDATE", "SELECT", "DELETE", "UPDATE"]
query_stats = {}
for qu in queries:
    if qu not in query_stats:
        query_stats[qu]=1
    else:
        query_stats[qu]+=1
print(query_stats)

#5 refresh day1
invoices = [
    {"client": "Austria_IT", "amount": 1200, "currency": "EUR"},
    {"client": "Poland_QA", "amount": 800, "currency": "USD"},
    {"client": "Local_Consult", "amount": 15000, "currency": "UAH"}
]

rates = {
    "USD": 39.0,
    "UAH": 1.0,
    "EUR": 42.5
}
total_uah = 0
for invoice_dict in invoices:
    total_uah += invoice_dict["amount"] * rates[invoice_dict["currency"]] 
    print(total_uah)

#1 day2
def calculate_net_income(amount, tax_rate=0.05):
    net_income = amount - amount * tax_rate
    return net_income

print(calculate_net_income(1000))

#2 day2
def wait_for_element(locator, timeout=5):
    if locator == "" :
        return False
    else:
        adequate_response = f"Очкування {locator} протягом {timeout} секунд"
        return adequate_response

print(wait_for_element(""))
print(wait_for_element("Mimimi"))

#3 day2
samba_conf = {"workgroup": "WORKGROUP", "security": "user"}
samba_conf2 = {"workgroup": "WORKGROUP", "security": "user", "guest_ok": 3}
key = "guest_ok"
def get_setting(config_dict, key):
    try:
        if isinstance(config_dict[key], str):
            return f"Рядок є рядок, а не щось інше! Дивись сам {config_dict[key]}"
        else:
            return f"Рядок не є рядок, а щось інше! Дивись сам -- {key}: {config_dict[key]}"
    except KeyError:
        return "Default Setting"

print(get_setting(samba_conf, key))
print(get_setting(samba_conf2, key))

#4 day2

def calculate_weekly_salary(hourly_rate, hours=40):
    try:
        num_rate = float(hourly_rate)
        num_hours = float(hours)
        result = num_rate * num_hours
        return result
    except TypeError:
        return f"Помилка! Рейт має бути числом, а не {type(hourly_rate)}"
    except ValueError:
        return f"не можливо обробити значення для hourly_rate = {hourly_rate}"

#ТЕСТИ
print(calculate_weekly_salary({"a":8.112})) # Виведе: Помилка TypeError... словник
print(calculate_weekly_salary(9))           # Виведе: 360.0
print(calculate_weekly_salary("25"))        # Виведе: 1000.0 (успішно перетворило рядок на число)
print(calculate_weekly_salary("25 USD"))    # Виведе: Помилка ValueError...
print(calculate_weekly_salary([25]))        # Виведе: Помилка TypeError...
print(calculate_weekly_salary(0))           # Виведе: 0.0 (пастка нуля пройдена)

#5 day2
layers = ["Base", "Nav", "Sym", "Num", 7]
def get_layer_name(layers_list, index):
    try:
        if isinstance(layers_list[index],str):
            return layers_list[index]
        else:
            return f"Помилка: назва шару має не строковий тіп. Назва: {layers[index]}" 
    except IndexError:
        return "Помилка: такого шару не існує"  

print(get_layer_name(layers, 0))
print(get_layer_name(layers, 1))
print(get_layer_name(layers, 2))
print(get_layer_name(layers, 3))
print(get_layer_name(layers, 4))
print(get_layer_name(layers, 5))

#6 day2
def parse_bpm(bpm_string):
    try:
        return int(bpm_string)
    except ValueError:
        return "0"

print(parse_bpm("110"))

#7 day2
#Perfect
job_perfect = {
    "title": "QA Automation Engineer",
    "location": "Warsaw, Poland",
    "company": "TechCorp",
    "salary": {
        "min": 3000,
        "max": 4000,          # <--- Ваша функція шукає саме це значення
        "currency": "EUR"
    }
}

#KeyError
# Варіант А: Є "salary", але роботодавець не вказав "max"
job_missing_max = {
    "title": "Manual QA",
    "location": "Vienna, Austria",
    "salary": {
        "min": 2500,
        "currency": "EUR"
        # Ключа "max" немає, виклик job_data["salary"]["max"] дасть KeyError
    }
}

# Варіант Б: Роботодавець взагалі нічого не написав про гроші
job_no_salary_at_all = {
    "title": "Junior Tester",
    "location": "Graz, Austria"
    # Ключа "salary" взагалі немає, виклик job_data["salary"] одразу дасть KeyError
}

#TypeError
job_bad_type = {
    "title": "Senior QA Engineer",
    "location": "Krakow, Poland",
    "salary": "Зарплата за результатами співбесіди" # <--- Це рядок (str), а не словник (dict)
}

def parse_salary_max(job_data):
    try:
        return job_data["salary"]["max"]
    except KeyError:
        return "There is no key [max]."
    except TypeError:
        if isinstance(job_data["salary"],str):
            return "Salary is lust a string. Not integer."

print(parse_salary_max(job_perfect))
print(parse_salary_max(job_missing_max))
print(parse_salary_max(job_no_salary_at_all))
print(parse_salary_max(job_bad_type))

#8 day2
# Вхідні дані для тестування
processes_data = [
    {"name": "xorg", "ram_mb": 120},                 # Нормальний процес (перевищує ліміт)
    {"name": "keyd", "ram_mb": 3},                   # Нормальний процес (в межах ліміту)
    {"name": "zombie_process"},                      # БИТИЙ: немає ключа ram_mb (викличе KeyError)
    {"name": "firefox-esr", "ram_mb": 450},          # Нормальний процес (перевищує ліміт)
    {"name": "htop", "ram_mb": 5},                   # Нормальний процес (в межах ліміту)
    {"name": "kernel_thread", "status": "sleeping"}, # БИТИЙ: є status, але немає ram_mb (викличе KeyError)
    {"name": "smbd", "ram_mb": "~1"}                   # Нормальний процес (в межах ліміту)
]

# Ліміт пам'яті для перевірки
memory_limit = 50

def filter_heavy_processes(process_list, max_ram):
    new_list = []
    for proc in process_list:
        try:
            if int(proc["ram_mb"]) > max_ram:
                new_list.append(proc["name"])
        except TypeError:
            print(f'не відповідний тип даних ram_mb для {proc["name"]}')
            continue
        except ValueError:
            print(f'не можливо обробити значення ram_mb для {proc["name"]}')
            continue
        except KeyError:
            print(f'відсутній ключ ram_mb для {proc["name"]}')
            continue
    return new_list

print(filter_heavy_processes(processes_data, memory_limit))

#9 day2
parts_prices = {
    "pcb_set": 15,          # Ціна за набір плат (в доларах)
    "choc_switches": 35,    # Ціна за пачку з 46 світчів
    "zmk_controller": 20,   # Ціна за пару мікроконтролерів
    "keycaps": "out_of_stock", # Немає в наявності (текст замість ціни)
    "case": None            # Ціна невідома (None замість ціни)
}

#all = parts.values()
#print(all)
def calculate_build_cost(parts_dict):
    total = 0
    for part_key, part_price in parts_dict.items():
        try:
            total += int(part_price)
        except TypeError:
            print(f'не відповідний тип даних {part_price} для {part_key}, або деталяка відсутня')
            continue
        except ValueError:
            print(f'не можливо обробити значення {part_price} для {part_key}, ціна вказана не цифрою')
            continue

    return total
test9day2 = calculate_build_cost(parts_prices)
print(test9day2)

#10 day2
# 1. Ідеальний сценарій: все на місці, статус 200
response_perfect = {
    "status": 200,
    "data": {
        "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    }
}

# 2. Логічна відмова: структура правильна, але статус не 200 (має повернути [])
response_404 = {
    "status": 404,
    "data": {
        "users": []
    },
    "error": "Not Found"
}

# 3. KeyError (немає статусу): бекенд взагалі забув передати "status"
response_missing_status = {
    "data": {
        "users": [{"id": 3, "name": "Charlie"}]
    }
}

# 4. KeyError (немає data): статус 200 є, але ключ "data" відсутній
response_missing_data = {
    "status": 200,
    "message": "OK, but no data provided"
}

# 5. KeyError (немає users): всередині "data" є що завгодно, крім "users"
response_missing_users = {
    "status": 200,
    "data": {
        "pagination": {"page": 1, "total_pages": 5},
        "settings": "dark_mode"
    }
}

# 6. TypeError (зламана структура): замість словника в "data" прийшов просто текст
response_type_error = {
    "status": 200,
    "data": "Internal Server Error in database connection"
}
#-----------------------------------#
def safe_get_users(response):
    try:
        if response["status"] == 200:
            return response["data"]["users"]
        else:
            return []
    except KeyError:
        "немає статус-коду, немає ключа data чи users"
        return []
    except TypeError:
        "структура data зламана"
        return []
#----------------------------------#
# Збираємо всі тестові відповіді в один список
all_tests = [
    response_perfect, 
    response_404, 
    response_missing_status, 
    response_missing_data, 
    response_missing_users, 
    response_type_error
]

# Проганяємо через вашу функцію
for i, test_data in enumerate(all_tests, 1):
    result = safe_get_users(test_data)
    print(f"Тест {i}: {result}")



