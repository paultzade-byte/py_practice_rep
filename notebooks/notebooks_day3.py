#1 refresh day2
p = 666
dlist=[1,2,1,3,2,4,5,p,5,66,3,6,7,2,7,8,4,9,0,5,6,'j', 'j', p]

def find_duplicates(data_list):
    duplicate_list = []
    for d_item in data_list:
        if data_list.count(d_item) > 1 and d_item not in duplicate_list: # Перевіряє чи елементів більше за один  
            duplicate_list.append(d_item)                                #і чи його ще нема в результуючому списку
        else:                                                            
            continue
    return duplicate_list
print(find_duplicates(dlist))

#2 refresh day2
tests = [
    {"name": "test_login", "status": "passed"},
    {"name": "test_payment", "status": "failed"},
    {"name": "test_registration", "status": "passed"},
    {"name": "test_logout", "status": "failed"},
    {"name": "test_cart_api", "status": "skipped"},
    {"name": "test_search", "status": "failed"},
    {"name": "test_profile_update", "status": "in_progress"},
    {"name": "test_payment", "status": "failed"}  # Дублікат для перевірки унікальності
]

def failed_status_dic_return(dic_list):
    res_list = [item["name"] for item in dic_list if item["status"] == "failed"]
    return res_list

print(failed_status_dic_return(tests))


#3 refresh day2

status_list = [200, 404, 200, 500, 201, 201, 300, 301, 405, 404, 500, 201, 100, 403, 404, 501, 205, 101, 100, 201]

def dict_maker(list_repeater):
    counter_dict = {}
    for i in list_repeater:
        if i not in counter_dict:
            counter_dict[i] = 1
        else:
            counter_dict[i] += 1
    return counter_dict

print(dict_maker(status_list))


#4 refresh day2


#5 refresh day2
def isvalid_email(email):
    EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._%+-]*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$"
    )

    try
    invalid_users = [item for item in pre_dict if ("mail" not in item or not isinstance(item["mail"],str) or not EMAIL_PATTERN.fullmatch(item["mail"]))]






#1 group writing files day3

error_messages = [
    "404 Not Found: Requested URL /api/v1/users/42 was not found on this server.",
    "500 Internal Server Error: Database connection timeout failed after 30000ms.",
    "401 Unauthorized: Invalid or expired JSON Web Token (JWT) provided.",
    "403 Forbidden: User 'john_doe' does not have permission to delete this record.",
    "422 Unprocessable Entity: Password must contain at least one special character.",
    "400 Bad Request: Missing required field 'email' in registration payload.",
    "503 Service Unavailable: Payment gateway is temporarily overloaded.",
    "408 Request Timeout: Client did not send a request within the time allowed by the server.",
    "404 Not Found: Image profile_pic.jpg could not be retrieved from AWS S3 bucket.",
    "500 Internal Server Error: NullPointerException in UserAuthService.java at line 142."
]


#with open('errors.txt', 'w', encoding='utf-8') as f:
#    for item in error_messages:    
#        f.write(item + '\n')

# коротший метод запису якщо в циклі треба тільи дія запису
with open('errors.txt', 'w', encoding='utf-8') as f:
    f.writelines(item + '\n' for item in error_messages)


with open('errors.txt', 'r', encoding='utf-8') as f:
    content = f.read()
print(content)


#2 group writing files day3

error_messages = [
    "404 Not Found: Requested URL /api/v1/users/42 was not found on this server.",
    "500 Internal Server Error: Database connection timeout failed after 30000ms.",
    "401 Unauthorized: Invalid or expired JSON Web Token (JWT) provided.",
    "403 Forbidden: User 'john_doe' does not have permission to delete this record.",
    "422 Unprocessable Entity: Password must contain at least one special character.",
    "400 Bad Request: Missing required field 'email' in registration payload.",
    "503 Service Unavailable: Payment gateway is temporarily overloaded.",
    "408 Request Timeout: Client did not send a request within the time allowed by the server.",
    "404 Not Found: Image profile_pic.jpg could not be retrieved from AWS S3 bucket.",
    "500 Internal Server Error: NullPointerException in UserAuthService.java at line 142."
]

# перезапис на випадок експериментів
#
with open('errors.txt', 'w', encoding = 'utf-8') as f:
    f.write('')

# основна функція дозапису
def log_event(message, log_amount):
    with open('errors.txt', 'a', encoding = 'utf-8') as f:
        i = 0
        for mes in message:
            f.write(f'[LOG]: {mes}\n')
            i+=1
            if i >= log_amount:
                break
    return

# функція читання файла
def event_read(message, log_amount):
    log_event(message, log_amount)
    with open('errors.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    return content

print(event_read(error_messages, 3))

#2 group writing files day3 (with universal slices method)

error_messages = [
    "404 Not Found: Requested URL /api/v1/users/42 was not found on this server.",
    "500 Internal Server Error: Database connection timeout failed after 30000ms.",
    "401 Unauthorized: Invalid or expired JSON Web Token (JWT) provided.",
    "403 Forbidden: User 'john_doe' does not have permission to delete this record.",
    "422 Unprocessable Entity: Password must contain at least one special character.",
    "400 Bad Request: Missing required field 'email' in registration payload.",
    "503 Service Unavailable: Payment gateway is temporarily overloaded.",
    "408 Request Timeout: Client did not send a request within the time allowed by the server.",
    "404 Not Found: Image profile_pic.jpg could not be retrieved from AWS S3 bucket.",
    "500 Internal Server Error: NullPointerException in UserAuthService.java at line 142."
]

# перезапис на випадок експериментів
#
with open('errors.txt', 'w', encoding = 'utf-8') as f:
    f.write('')

# основна функція дозапису |  universal slices method
def log_event(message, log_amount):
    with open('errors.txt', 'a', encoding='utf-8') as f:
        # Беремо лише перші 333 елементи (якщо у списку їх менше, запише скільки є)
        for mes in message[2:log_amount:4]:
            f.write(f'[LOG]: {mes}\n')
    return


# функція читання файла
def event_read(message, log_amount):
    log_event(message, log_amount)
    with open('errors.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    return content
    
print(event_read(error_messages, 3))
print(' ')
print(event_read(error_messages, 333))



#1 group classes day3
name_of_test_my = 'namema'
status_of_test_my = 'pissed'

class TestReport:
    def __init__(self, test_name, status):
        self.test_name = test_name
        self.status = status
    def print_summary(self):
        return f"Test {self.test_name} finished with status: {self.status}"

print(TestReport(name_of_test_my, status_of_test_my).print_summary())

#1 group classes day3 (сучасний варіант)

from dataclasses import dataclass

name_of_test_my = 3
status_of_test_my = 'pissed'

@dataclass
class TestReport:
    # Просто вказуємо змінні та їхні типи даних
    test_name: str
    status: str

    def print_summary(self):
        return f"Test {self.test_name} finished with status: {self.status}"

# Створення об'єкта працює точно так само, як і раніше
print(TestReport(name_of_test_my, status_of_test_my).print_summary())
print(type(TestReport(name_of_test_my, status_of_test_my).test_name))

#2 group classes day3
# old method
class WebElement:
    def __init__(self, locator, is_visible=False):
        self.locator = locator
        self.is_visible = is_visible
    def click(self):
        if self.is_visible:
            return f"Clicking element {self.locator}"
        else:
            return "Error: element is not visible"
print(WebElement(".sulfulator").click())
print(WebElement(".sulfulator", True).click())

#2 group classes day3
#new method
from dataclasses import dataclass

@dataclass
class WebElement:
    locator: str
    is_visible: bool = False

    def click(self):
        if self.is_visible:
            return f"Clicking element {self.locator}"
        else:
            return "Error: element is not visible"

print(WebElement('tmm').click())
print(WebElement('tmm', True).click())

#3 group classes day3

from dataclasses import dataclass 
password_from_base = '12345'
@dataclass
class User:
    email: str
    password_from_base: str
    password_from_user: str
    new_password: str
    
    def change_password(self):
        if self.password_from_base == self.password_from_user:
            self.password = self.new_password
            return self.password
        else:
            return "Error: invalid password! Try again!"

print(User('email@mail.cum', password_from_base, '12345', '54321').change_password())
print(User('email@mail.cum', password_from_base, '1235', '5321').change_password())
    

#4 group classes day3

from dataclasses import dataclass 
password_from_base = '12345'
@dataclass
class User:
    user_mail: str
    password_from_base: str

    def return_email(self):
        return self.user_mail

user1 = User('mail@mail1.cum', '12341')
user2 = User('mail@mail2.cum', '12342')
user3 = User('mail@mail3.cum', '12343')
user_list =[
    user1, user2, user3
]

for i in range(len(user_list)):
    print(user_list[i].return_email() + 'called as method')
    print(user_list[i].user_mail + 'called as attribute')

#5 group classes day3

from dataclasses import dataclass, field

@dataclass
class TestCase:
    step_name: str
    steps: list = field(default_factory=list)

    def add_step (self):
        self.steps.append(self.step_name)
        return self.steps

    def run(self):
        result = []
        for e in range(len(self.steps)):
            result.append(f"Executing: {self.steps[e]}")
        return result
        
list_my = ['22','33']
print(TestCase('ii', list_my).add_step())

#6 group classes day3

from dataclasses import dataclass

@dataclass
class APIClient:
    base_url: str
    endpoint: str
    payload: str
    
    def get_point(self):
        url = self.base_url + self.endpoint
        return url
    def post(self):
        return f"POST до {self.get_point()} з даними {self.payload}"
        

client = APIClient("https://example.com", "/users", "{'name': 'Alex'}")
print(client.post())

#7 group classes day3

from dataclasses import dataclass

class Session:
    total_sessions = 0
    def __init__(self):
        Session.total_sessions +=1
    def return_total(self):
        return self.total_sessions

obj1 = Session()
obj2 = Session()
obj3 = Session()

print(Session().return_total())

#7 group classes day3 (new method / more Pythonic)
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Session:
    # ClassVar = спільна змінна класу!"
    total_sessions: ClassVar[int] = 0
    
    # Інші поля об'єкта (якщо є) писалися б тут, наприклад:
    # user_id: str

    def __post_init__(self):
        # Цей метод датаклас викликає автоматично ОДРАЗУ після  __init__
        Session.total_sessions += 1

    @classmethod
    def return_total(cls):
        return cls.total_sessions

# Перевіряємо роботу:
obj1 = Session()
obj2 = Session()
obj3 = Session()

# Викликаємо правильний метод класу БЕЗ створення нових об'єктів
print(Session.return_total())  # Виведе: 3


#8 group classes day3

from dataclasses import dataclass

@dataclass
class Browser:
    name: str = "Chrome"
    is_open: bool = False
    
    def __post_init__(self):
        pass
    
    def open_browser(self):
        self.is_open = True
        return self.is_open

    def close_browser(self):
        self.is_open = False
        return self.is_open
        
print(Browser().open_browser())
print(Browser().close_browser())

#9 group classes day3

from dataclasses import dataclass

@dataclass
class BasePage:
    driver: str = "driver"
    url: str = "url"

    def open_page(self):
        return f"Opening {self.url}"

print(BasePage().open_page())

#10 group classes day3

from dataclasses import dataclass

username = 'vasua'
password = 'vavasusuaa'

@dataclass
class BasePage:
    username: str 
    password: str
    driver: str = "driver"
    url: str = "url"


    def open_page(self):
        return f"Opening {self.url}"

class LoginPage(BasePage):


    def login(self):
        print(f"Entering {self.username} and {self.password}")
        print("Clicking login button")
    

a = LoginPage(username, password) 
print(a.open_page())  #фішечка наслідування
a.login()

#11 group classes day3
username_from_database = 'vasua'
password_from_database = 'vavasusuaa'

# Забираємо @dataclass, робимо звичайний клас
class BasePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open_page(self):
        return f"Opening {self.url} with driver {self.driver} !"

class LoginPage(BasePage):
    def __init__(self, driver):
        # 1. Викликаємо батьківський __init__
        # 2. Передаємо йому драйвер, який прийшов
        # 3. ЖОРСТКО задаємо url саме для цієї сторінки
        super().__init__(driver=driver, url="/login")

    # Юзернейм і пароль передаємо сюди, бо це дія, яка стосується лише логіну!
    def login(self, username, password):
        print(f"Entering {username} and {password}")
        print(f"Clicking login button on the page with url {self.url}")


# Створюємо драйвер (поки що просто рядок-заглушка)
mock_driver = "Chrome"

# Створюємо екземпляр сторінки, передаючи ТІЛЬКИ драйвер
a = LoginPage(mock_driver) 

# Викликаємо метод з BasePage (твоя "фішечка")
print(a.open_page())  

# Викликаємо логін, передаючи дані з нашої "бази"
a.login(username_from_database, password_from_database)



