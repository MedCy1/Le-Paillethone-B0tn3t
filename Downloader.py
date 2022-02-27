



def Download(sock, args):
    filename = args.split(b'"')[1].decode('utf-8') #decode to string
    size = args.split(b' ')[2].split(b'\n')[0].decode("utf-8") #split size and decode to strign
    size = int(size) # cast to int

    #if we got data because of fast internet connection
    #or whatever may have happened

    data = '\n'.join(args.split(b'\n'[1:]))

    return _Download(sock , filename, size, data)

def _Download(sock, filename, size, data = b''):
    f = open(filename, 'wb')
    ldata = len(data)
    if ldata:
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