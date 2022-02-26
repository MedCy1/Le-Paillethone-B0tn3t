import socket
import os, sys
import _thread
import time

CLIENT_TIMEOUT =  30 # seconds
MAXIMUM_CLIENTS = 100 # seconds


# Common parts
cwd = os.getcwd()
os.chdir('..')
sys.path.append(os.getcwd())
os.chdir(cwd)

from Communicator import COMMUNICATOR

class SERVER:
    def __init__(self, ip, port):
        self.clients = {}

        sock = socket.socket()
        sock.bind((ip, port))

        global MAXIMUM_CLIENTS
        sock.listen(MAXIMUM_CLIENTS)

        self.sock = COMMUNICATOR(sock)


    # add a client to the list
    def UpdateClient(self, addr, conn):
        self.clients[addr] = (conn, time.time()) # Insert/Update client socket/time

    # Remove clients is passed the timeout
    def ClientTimeouts(self):
        todelete = []
        for k,v in self.clients.items():
            if time.time() - v[1] > CLIENT_TIMEOUT:
                todelete.append(k)

        for i in todelete:
            del self.clients[k]

    # Accept all clients
    def AcceptClients(self):
        while True:
            client = self.sock.accept()
            if client:
                self.UpdateClient(client[1], client[0])
            else:
                break
    
    def MainLoop(self):
        while True:
            os.system("cls")
            self.AcceptClients()
            self.ClientTimeouts()
            print(self.clients)


if __name__ == "__main__":
    s = SERVER('127.0.0.1', 8080)
    s.MainLoop()