import socket
import subprocess
from Communicator import COMMUNICATOR
from Downloader import Download

ALL_ACTIONS = {

}

if __name__ == "__main__":
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8080))
        sock = COMMUNICATOR(sock)
        while True:
                d = sock.recv()
                if d == b'':
                        sock.close()
                        break
                try:
                        d = d.decode('utf-8')
                        d = d.split(' ') # split all arguments/commands
                        if d in ALL_ACTIONS:
                                ALL_ACTIONS[d]()
                except:
                        pass