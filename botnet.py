import socket
import subprocess
from Communicator import COMMUNICATOR



if __name__ == "__main__":
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8080))
        sock = COMMUNICATOR(sock)
