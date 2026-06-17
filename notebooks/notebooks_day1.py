#0
result_list = []
pre_dict = [
    {"name": "vasua", "age": 25},
    {"name": "vasua1", "age": 25},
    {"name": "vasua2", "age": 75},
    {"name": "vasua3", "age": 35},
    {"name": "vasua4", "age": 15}
]

for user in pre_dict:
    if user["age"] >= 18:
        result_list.append(user)

print(result_list)

#1
addrlist = ['192.168.1.1','192.168.0.1','92.68.22.45','192.168.22.1','12.16.1.12','19.168.1.1','192.18.1.1']
resultlist=[]
for i in addrlist:
    if i.startswith("192.168"):
        resultlist.append(i)
print(resultlist)

#2
username_email = [
    "uname:email@nail.cum",
    "uname1:email1@nail.cum",
    "uname2:email2@nail.cum",
    "uname3:email3@nail.cum",
    "uname4:email4@nail.cum",
    "uname5:email5@nail.cum",
    "uname6:email6@nail.cum"
]
new_mail_list = []
for i in username_email:
    name, email = [namemail.strip() for namemail in i.split(':')]
    new_mail_list.append(email)
print(new_mail_list)


#3
test_result_list = [
    {"test_name": "login0", "status": "failed", "duration": 3.0},
    {"test_name": "login1", "status": "success", "duration": 4.5},
    {"test_name": "login2", "status": "failed", "duration": 2.5},
    {"test_name": "login3", "status": "failed", "duration": 4.5},
    {"test_name": "login4", "status": "success", "duration": 1.5},
    {"test_name": "login5", "status": "failed", "duration": 1.5},
    {"test_name": "login6", "status": "success", "duration": 4.5},
    {"test_name": "login7", "status": "success", "duration": 3.5},
    {"test_name": "login8", "status": "failed", "duration": 4.5},
]

for i in test_result_list:
    if i["status"] == "failed" and i["duration"] > 3.0:
        print(i["test_name"])

#4
import re

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._%+-]*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$"
)

pre_dict = [
    {"name": "vasua", "age": 25, "mail":"_@-.cum"},
    {"name": "vasua1", "age": 25, "mail":"sobakabubaka@gmail.culjm"},
    {"name": "vasua2", "age": 75, "mail":"NULL"},
    {"name": "vasua3", "age": 35},
    {"name": "vasua4", "age": 15, "mail":None}
]

invalid_users = [item for item in pre_dict if ("mail" not in item or not isinstance(item["mail"],str) or not EMAIL_PATTERN.fullmatch(item["mail"]))]
print(invalid_users)

#5
port_list = [
    {"port": 22, "state": "open", "service": "ssh"},
    {"port": 2020, "state": "close", "service": "ssh"},
    {"port": 1122, "state": "open", "service": "ssh"},
    {"port": 2112, "state": "close", "service": "ssh"},
    {"port": 1333, "state": "open", "service": "ssh"},
    {"port": 1322, "state": "close", "service": "ssh"},
    {"port": 1500, "state": "open", "service": "ssh"},
    {"port": 1343, "state": "close", "service": "ssh"},
    {"port": 80, "state": "open", "service": "ssh"},
    {"port": 222, "state": "open", "service": "ssh"}
]

result_list = [item for item in port_list if (item["state"] == "open" and item["port"] > 1024)]
print(result_list)

#6
transaction_list = [15000, 15000, 22000, 8500, 8999, 66555, 88.89, 900]
total_tax = 0
for i in transaction_list:
    total_tax = total_tax + 0.05*i
print(total_tax)

#7
http_statuscode_list = [200, 404, 200, 500, 401, 200, 404, 204, 403, 501, 300, 201, 404,
                       501, 404, 200, 302, 205, 101, 101, 101, 101, 400, 403, 201, 501]
status_counts = {}

for i in http_statuscode_list:
    if i not in status_counts:
        status_counts[i]=1
    else:
        status_counts[i]+=1
print(status_counts)

#8
keys = ["host", "port", "user"]
values = ["10.0.0.5", 22, "admin"]
keyvalue_dict = {}
for i in range(len(keys)):
    keyvalue_dict[keys[i]]=values[i]
print("keyvalue_dict: ",keyvalue_dict)
#-------------------------------#
keyvalue_dict2 = dict(zip(keys,values))
print("keyvalue_dict2: ",keyvalue_dict)

#9
retries = 0
max_retries = 5
while retries < max_retries:
    if retries == 3:
        print('Підключення успішне')
        break
    else:
        print('Спроба підключення...')
    retries+=1

#10
list_old = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}, {"id": 1, "name": "A"}]
list_new = []
for i in range(len(list_old)):
    if list_old[i] not in list_new:
        list_new.append(list_old[i])
    else:
        print('Duplicot found! ', list_old[i], 'already exists. Issue located at posision', i+1, )
print('list_new: ', list_new)



