import socket
import os, sys
import _thread
import time
import queue

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

    def SendToClients(self, data):
        for i in self.clients:
            sock = i[0]
            sock.send(data)
    
    def MainLoop(self, in_, out_):
        while True:
            self.AcceptClients()
            self.ClientTimeouts()
            if out_.qsize == 0:
                out_.put(self.clients)

            data = self.DataToSend.get(False)
            self.SendToClients(self.DataToSend)

            try:
                data = self.DataToSend.get(False)
                print(data)
            except:
                EnableInput = True
            else:
                EnableInput = False
                self.SendToClients(data)

            if EnableInput:
                try:
                    i = in_.get(False)
                except:
                    pass
                else:
                    print("Got Input")
                    li = i.split(' ') [0]
                    if li[0] in self.ACTIONS:
                        self.ACTIONS[li[0]](i)


    ####### Action #######
    # This send file
    def _SendFile(self, path, sendQ):
        path = path.replace('\\', '/') # make sure path is in linux form
        name = path.split('/') # get the name
        size = os.path.getsize(path)[-1]
        print('SENDING DOWNLOAD EVENT')
        sendQ.put(f'DOWNLOAD "{name}" {size}\n') # \n is for detecting when the header stops
        f = open(path, 'rb')
        while f:
            data = f.read(SEND_FILE_BUFFER)
            sendQ.put(data)
        f.close()
    # laucher to send files
    def SendFile(self, path):
        inp = inp.split(' ')
        if len(inp) > 1:
            path = ' '.join(inp[1:])
        else:
            print('PATH NOT INITIALIZED')
            return 1
        print("Sending")         
        _thread.start_new_thread(self._SendFile(path, self.DataToSend))

if __name__ == "__main__":
    s = SERVER('127.0.0.1', 8080)
    in_ = queue.Queue()
    out_ = queue.Queue()
    _thread.start_new_thread(s.MainLoop, (in_, out_))

    while True:
        os.system("cls")
        i = input('> ')
        if i:
            input(i)