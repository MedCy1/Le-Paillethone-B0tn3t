import socket
import os, sys
import _thread
import time


CLIENT_TIMEOUT = 30 # seconds
MAXIMUM_CLIENTS = 100 #seconds

#Common parts
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

    def UpdateClient(self, addr, conn):
        if addr not in self.client.key():
            self.clients[addr] = (conn, time.time())     


    def ClientTimeout(self):
        todelete = []
        for k,v in self.clients.items():
            if time.time() - v[2] > CLIENT_TIMEOUT:
                todelete.append(k)


        for i in todelete:
            del self.clients[k]


    def AcceptClients(self):
        while True:
            client = self.sock.AcceptClient()
            if client:
                self.UpdateClient(client[1], client[0])
            else:
                break    


    def MainLoop(self):
        while True:
            os.system('cls')
            self.AcceptClients()
            self.ClientTimeout()
            print(self.clients)




if __name__ == "__main__":
    s = SERVER("127.0.0.1", 8080)
    s.MainLoop()