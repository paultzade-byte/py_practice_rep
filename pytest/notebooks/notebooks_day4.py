#примітка для вирішення проблем з кешем jupyter notebook
# якщо видалив тест (функцію) а при запуску вона все одно пишеться, то виконай цю комірку

import piplite
await piplite.install(['pytest', 'ipytest'])

# ОБОВ'ЯЗКОВО імпортуємо заново після перезапуску ядра
import pytest
import ipytest

# Очищаємо кеш ipytest про всяк випадок
ipytest.clean()
ipytest.autoconfig()

@pytest.fixture
def test_user():
    return {"username": "tester", "status": "active"}

def test_user_status(test_user):
    assert test_user["status"] == "active"

ipytest.run()


#1 day4
import pytest
import ipytest

ipytest.autoconfig()

@pytest.fixture
def greeting():
    b = "Hello, Pytest!"
    return b

def test_greeting_ok(greeting):
    assert "Hello, Pytest!" in greeting , "vse ne ok"
    

ipytest.run()

#2 day4
import piplite
await piplite.install(['pytest', 'ipytest'])

ipytest.autoconfig()

@pytest.fixture
def test_user():
    dic = {"username": "tester", "status": "active"}
    return dic
    
def test_dic_user(test_user):
    assert test_user["status"] == "active", "Ne, ne active!"

ipytest.run("-k dic_user")

#3 day4
import piplite
await piplite.install(['pytest', 'ipytest'])

ipytest.autoconfig()

@pytest.fixture
def host():
    local_host = "localhost"
    return local_host

@pytest.fixture
def port():
    p = 8080
    return p

def test_connection_string(host, port):
    assert f"{host}:{port}" == "localhost:8080"
    
ipytest.run("-k test_connection_string")

#4 day4
import piplite
await piplite.install(['pytest', 'ipytest'])

ipytest.autoconfig(clean=True)

@pytest.fixture
def host():
    local_host = "localhost"
    return local_host

@pytest.fixture
def port():
    p = 8080
    return p

@pytest.fixture
def server_url(host, port):
    a = f"http://{host}:{port}"
    return a

def test_connection_string2(server_url):
    assert server_url == "http://localhost:8080"
#ipytest.run()    
ipytest.run("-k test_connection_string2")

#5 day4
import piplite
await piplite.install(['pytest', 'ipytest'])

ipytest.autoconfig(clean=True)

@pytest.fixture
def file_mock():
    print("Opening file...")
    a = "data"
    yield a
    print("\nClosing file...")

def test_run(file_mock):
    print(file_mock+'1')
    print("test in process")
    print(file_mock+'2')
    assert file_mock == "data" , "everything is not ok"
    print(file_mock+'3')
    assert file_mock+"333" == "data333" , "everything is not ok"
    print("after test")
ipytest.run("-sk test_run")

#6 day4
import piplite
await piplite.install(['pytest', 'ipytest'])

ipytest.autoconfig(clean=True)

@pytest.fixture
def numbers_list():
    a = [1, 2, 3, 4, 5]
    return a
    
def test_run11(numbers_list):
    assert len(numbers_list) == 5 

def test_run12(numbers_list):
    assert sum(numbers_list) == 15
    
ipytest.run("-sk test_run1")

#7 day4
import piplite
await piplite.install(['pytest', 'ipytest'])

ipytest.autoconfig(clean=True)

@pytest.fixture(scope="session")
def session_id():
    # Цей прінт покаже, скільки разів викликається фікстура
    print("\n=== ГЕНЕРУЮ ID ДЛЯ ВСІЄЇ СЕСІЇ (1 РАЗ) ===")
    a = 777
    return a
    
def test_run_1(session_id):
    assert session_id == 777 

def test_run_2(session_id):
    assert session_id == 777
    
ipytest.run("-sk test_run_")

#7 day4 
# + додано лічильник щоб мати відображення кількості звернень до фікстури
import pytest
import ipytest

ipytest.autoconfig(clean=True)


# функційний скоуп - по дефолту, але для скоупа session лічильник працює 1 раз(1 сесія)
@pytest.fixture(scope="function") 
def session_id(request):
    # Перевіряємо, чи вже створено лічильник у сесії, якщо ні — ставимо 0
    if not hasattr(request.config, "fixture_calls"):
        request.config.fixture_calls = 0
        
    request.config.fixture_calls += 1 
    b = request.config.fixture_calls
    a = 777
    return a, b
    
def test_run_1(session_id):
    print(f"\n test_run_1 отримав номер виклику: {session_id[1]}")
    assert session_id[0] == 777 

def test_run_2(session_id):
    print(f"\n test_run_2 отримав номер виклику: {session_id[1]}")
    assert session_id[0] == 777
    
ipytest.run("-sk test_run_")
# якщо запускати кожен тест окремо через ipytest.run() 
# то лічильник буде обнулятись і давати 1

#8 day5
import pytest
import ipytest

ipytest.autoconfig(clean=True)

@pytest.fixture(autouse=True)
def log_test_start ():
    print("--- Test Started ---")

def test_empty_first():
    assert True

def test_empty_second():
    assert True 

ipytest.run("-sk test_empty_")



#9 day5
import pytest
import ipytest

ipytest.autoconfig(clean=True)
@pytest.fixture
def coordinates():
    a = (10, 20)
    return a

def test_9(coordinates):
    x = coordinates[0]
    y = coordinates[1]
    assert x < y, "no, really x >= y"

ipytest.run("-sk test_9") 

#10 day5

import pytest
import ipytest

ipytest.autoconfig(clean=True)
@pytest.fixture
def zero_value():
    return 0

def test_division_by_zero(zero_value):
    with pytest.raises(ZeroDivisionError) as zerodiv:
        a = 1 / zero_value

    assert zerodiv.type is ZeroDivisionError

ipytest.run("-sk test_division_")



#11 h day5


# Мета задачі: переконатися на практиці, 
# що фікстура з дефолтним scope="function" 
# створює чистий стан (новий словник) для кожного окремого тесту.
import pytest
import ipytest

ipytest.autoconfig(clean=True)
@pytest.fixture
def mock_db():
    return {"users": []}

def test_123(mock_db):
    mock_db["users"].append("user1") # звернення до фікстури як до словника, що має порожній список у елементі users
    print(mock_db)
    assert len(mock_db["users"]) == 1, "length is not equal to 1"

def test_124(mock_db):
    mock_db["users"].append("user2")
    print(mock_db)
    assert len(mock_db["users"]) == 1, "length is not equal to 1"

ipytest.run("-sk test_12")

#12 h day5

import pytest
import ipytest

ipytest.autoconfig(clean=True)
@pytest.fixture
def base_url():
    return "https://api.myproject.com/v1"

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer token123"}

@pytest.fixture
def api_client(base_url, auth_headers):
    return {"url": base_url, "headers": auth_headers}

def test_mytest1(api_client):
    assert api_client["headers"]["Authorization"] == "Bearer token123", "Bearer token mismatch issue!!!"

ipytest.run("-sk test_mytest1")

#13 h day5

import pytest
import ipytest

ipytest.autoconfig(clean=True)
@pytest.fixture
def browser_session():
    print("Відкриття браузера...")
    a = {"browser": "chrome", "is_open": True}
    yield a
    a["is_open"] = False
    print("Закриття браузера...")
    print(a)

def test_inside_1(browser_session):
    assert browser_session["is_open"] == True , "ioiiooo"

ipytest.run("-sk test_inside_1")

#14 h day5
# далі буде просто репринт від АІ
import pytest
import ipytest
username = "adm0in"
def create_user(username):
    if username in ["admin","root"]:
        raise ValueError("Ім'я заборонено")
    return f"Користувача {username} створено"

ipytest.autoconfig(clean=True)
@pytest.fixture
def restricted_names():
    return ["admin", "root"]

def test_restrict(restricted_names):
    for name in restricted_names: # звернення до фікстури як до списку бо вона поввертає список
        with pytest.raises(ValueError) as val_ures:
            create_user(username)
        assert a == restricted_names , "Everything is ok"
    
ipytest.run("-k test_restrict")

# 14 h day5
# репринт від АІ 

import pytest 
import ipytest
# ім'я-симуляція реального імені яке буде введено на фронт-енді
usern = "ordinary_user"
# ========================================== #
# блок-симуляція фронтенд та бекенд сайту    #
# ========================================== #
# резервація імен (в реальному житті - конфіг файл)
reserved_names = {"admin", "root", "superuser", "administrator"}

# функція перевірки та "створення" користувача
def create_user(username):
    if username.lower().strip() in reserved_names:
        raise ValueError("Ім'я заборонено")
    return f"Користувача {username} успішно створено "

# ========================================== #
# безпосередньо блок тесту                   #
# ========================================== #

ipytest.autoconfig(clean=True)

# фікстура яка параметризує тест
@pytest.mark.parametrize("test_name", ["admin", "root", "superuser"])
def test_13_restricted_name(test_name):
    # перевірка наявності помилки та метчу тексту з вимогами 
    with pytest.raises(ValueError, match="Ім'я заборонено"):
    # для реального сайта тут викликається 
        create_user(test_name)

# Обов'язково додаємо позитивний тест (Happy Path), 
# щоб впевнитися, що система взагалі дозволяє створювати користувачів.
def test_13_valid_user_creation_is_successful():
    result = create_user(usern)
    assert result == f"Користувача {usern} успішно створено "


# Запуск тестів
ipytest.run("-k test_13_")

#14 приклад "з життя" для наглядності

import pytest
import requests

# URL нашого API на тестовому сервері
API_URL = "https://dev.mysite.com/api/v1/users/register"

@pytest.mark.parametrize("test_name", ["admin", "root", "superuser"])
def test_api_restricted_names_are_blocked(test_name):
    # 1. Формуємо такі ж дані, які б відправив браузер (JSON)
    payload = {
        "username": test_name,
        "password": "secure_password123"
    }

    # 2. РОБИМО ВИКЛИК АПІ МЕТОДУ (замість create_user)
    response = requests.post(API_URL, json=payload)

    # 3. Перевіряємо результат
    # У вебі замість ValueError сервер має повернути правильний HTTP статус-код.
    # 400 Bad Request — стандартна відповідь, якщо клієнт надіслав невалідні дані.
    assert response.status_code == 400
    
    # Перевіряємо, що бекенд віддав фронтенду правильний текст помилки
    assert response.json()["error"] == "Ім'я заборонено"

# Позитивний тест
def test_api_valid_user_creation():
    response = requests.post(API_URL, json={"username": "ordinary_user", "password": "123"})
    
    # 201 Created — успішне створення ресурсу
    assert response.status_code == 201 
    assert response.json()["message"] == "ОК"

#15 h day5
# Мета задачі: побачити, як scope відмінний від function 
# і як він дозволяє тестам ділити спільний стан та змінювати його.
import pytest
import ipytest

ipytest.autoconfig(clean=True)

@pytest.fixture(scope="module")
def global_counter():
    a = [0]
    yield a
    #a.clear()
    a[0] = 0
    
def test_primat1233(global_counter):
    global_counter[0] += 1 # звернення до елемента списку бо фікстура повертає список з елементом 0
    assert global_counter[0] == 1 , "oj vsio"

def test_primat1234(global_counter):
    global_counter[0] += 1
    assert global_counter[0] == 2 , "oj vsio"

ipytest.run("-sk test_primat123")



#16 vh day5

import pytest, ipytest

ipytest.autoconfig(clean=True)

@pytest.fixture
def user_factory():
    def inner_func(username, role="user"):
        return {"username": username, "role": role}
    return inner_func 

def test_omanacoi_inner(user_factory):
    admin_user = user_factory("admin", "adminrole") # ти можеш звертатись до фікстури як до функції бо вона повертає це
    guest_user = user_factory("guest", "guestrole")
    user_user = user_factory("user")
    assert admin_user == {"username": "admin", "role": "adminrole"}
    assert guest_user == {"username": "guest", "role": "guestrole"}
    assert user_user == {"username": "user", "role": "user"}

ipytest.run("-sk test_omanacoi_inner")


#17 day6
# якщо треба взяти з бази дані а потім відкотити їх до передтестового стану

import pytest, ipytest

ipytest.autoconfig(clean=True)

@pytest.fixture(scope="module")
def global_db():
    return {"users_count": 10}

@pytest.fixture(scope="function")
def db_transaction(global_db):
    mem_count = global_db["users_count"]
    print('db_transaction before yield = ', mem_count)
    yield global_db
    global_db["users_count"] = mem_count
    print('db_transaction after yield = ', global_db["users_count"])
# tests

def test_mem_count_1(db_transaction):
    db_transaction["users_count"] += 5
    print('db_transaction in test_mem_count_1 = ', db_transaction)
    assert db_transaction["users_count"] == 15, "AHUET!"

def test_mem_count_2(db_transaction):
    print('db_transaction in test_mem_count_2 = ', db_transaction)
    assert db_transaction["users_count"] == 10, "AHUETT!!"


ipytest.run("-sk test_mem_count_")

#18 day6
# лімітер, що обмежує кількість апі запитів або інших дій

import pytest, ipytest
ipytest.autoconfig(clean=True)

# simulated config
api_state = {"requests_left": 2}

# simulated backend
@pytest.fixture(scope="module")
def make_request(api_state):
    if  api_state["requests_left"] > 0:
        api_state["requests_left"] -= 1
        yield "Success"
    elif api_state["requests_left"] == 0:
        yield PermissionError("Limit exceeded")
    elif api_state["requests_left"] < 0 or type(api_state["requests_left"]) != int:
        yield ValueError("Invalid limit count. Call to administrator.")
    print("program is finished, api_state limiter take it's default value")
    api_state["requests_left"] = 2

# tests
        
def limiter_test_1(make_request):
    assert make_request == "Success", "not a success"

def limiter_test_2(make_request):
    assert make_request == "Success", "not a success"

def limiter_test_3(make_request):
    with pytest.raises(PermissionError, match="Limit exceeded"):
        make_request()

ipytest.run()



