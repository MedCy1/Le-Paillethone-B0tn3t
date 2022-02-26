import socket
import os, sys
from symbol import pass_stmt
import _thread
import queue
import time

CLIENT_TIMEOUT =  30 # seconds
MAXIMUM_CLIENTS = 100 # seconds
SEND_FILE_BUFFER = 5120 # 5kb


# Common parts
cwd = os.getcwd()
os.chdir('..')
sys.path.append(os.getcwd())
os.chdir(cwd)

from Communicator import COMMUNICATOR

class SERVER:
    def __init__(self, ip, port):
        self.clients = {}
        self.ACTION = {
            'UPLOAD': self.SendFile,
        }

        sock = socket.socket()
        sock.bind((ip, port))

        global MAXIMUM_CLIENTS
        sock.listen(MAXIMUM_CLIENTS)

        self.sock = COMMUNICATOR(sock)
        self.DataToSend = queue.Queue()


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
    
    def MainLoop(self, in_, out_):
        while True:
            os.system("cls")
            self.AcceptClients()
            self.ClientTimeouts()
            if out_.qsize == 0:
                out_.put(self.clients)

            try:
                cmd = in_.get(False) # get without blocking
            except:
                pass

            if self.DataToSend


    ####### Action #######
    # This send file
    def SendFile(self, path):
        f = open(path, 'r')
        data = f.read(SEND_FILE_BUFFER)
        self.sock.send(data)



if __name__ == "__main__":
    s = SERVER('127.0.0.1', 8080)
    in_ = queue.Queue()
    out_ = queue.Queue()
    s.MainLoop(in_, out_)