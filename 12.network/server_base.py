
import socket

try:
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 80))
    server.listen(5) # max client

    # in your code

finally:
    # it will throw error OSError: [Errno 12] ENOMEM if your dont exec the code.
    server.close()
