




# Argument Parser
def Download(args, sock):
    filename = args.split(b'"')[1].decode('utf-8') # decode to string
    size = args.split(b' ')[2].split(b'\n').decode('utf-8') # split size and decode string
    size = int(size) # cast to int
    # if we got data because of fast internet connection
    # or watever may have happened
    data = b'\n'.join(args.split(b'\n')[1:])

    _Download(sock, filename, size, data)


# Actual download function
def _Download(sock, filename, size, data = b''):
    f = open(filename, 'wb')
    ldata = len(data)
    if ldata: # > 0
        f.write(data)
        data = b''

    while ldata < size:
        data = sock.recv()


        if not sock.IsConnected:
            return 1

        if data == b'':
            continue

        
        ldata += len(data)
        f.write(data)
        data = b''
    
    f.close()

    return 0