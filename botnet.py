import socket
from Communicator import COMMUNICATOR
from Downloader import Download

ALL_ACTIONS = {
        'DOWNLOAD': Download
}

if __name__ == "__main__":
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8080))
        sock = COMMUNICATOR(sock)
        while True:
                d = sock.recv()
                if not sock.IsConnected:
                        break
                if d != b'':
                        print(d)
                dlist = d.split(b' ') # split all arguments/command
                if dlist[0] in ALL_ACTIONS:
                        ALL_ACTIONS[dlist[0]](d, sock) # caLL function
