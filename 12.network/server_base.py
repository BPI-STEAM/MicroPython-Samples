
import socket

try:
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 80))
    server.listen(5) # max client

    # in your code

    while True:
        cl, addr = server.accept()
        print('client connected from', addr)
        
        buf = cl.recv()

        if b'open' in buf:
            print(b'open')

        cl.send(buf)
        cl.close()
finally:
    # it will throw error OSError: [Errno 12] ENOMEM if your dont exec the code.
    server.close()
