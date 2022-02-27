





def Download(args, sock):
    filename = args.split(b'"')[1].decode('utf-8') # decode to string
    size = args.split(b' ')[2].split(b'\n').decode('utf-8') # split size and decode string
    size = int(size) # cast to int
    # if we got data because of fast internet connection
    # or watever may have happened
    data = b'\n'.join(args.split(b'\n')[1:])

    _Download(sock, filename, size, data)

def _Download(sock, filename, size, data = b''):
    ldata = len(data)

    while ldata < size:
        d = sock.recv()