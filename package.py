

# def UartSlave():

#     def send():
#         pass

#     def recv():
#         pass

# import time
# from machine import UART

# uart = UART(2)  # UART(2) RX16 TX17

# # while True:
# #     recvlen = uart.any()
# #     if recvlen > 0:
# #         buffer = uart.read(recvlen)
# #         uart.write(buffer)
# #         print(buffer)

# #     uart.init(57600, bits=8, parity=None, stop=1)

# def UartHost():

#     def __init__(self, uart):
#         self.uart = uart
#         self.queue = []
#         self.result = {}

#     def run(self):
#         eof, cmd = None, None
#         while True:

#             if cmd is None and len(self.queue) > 0:
#                 cmd = self.queue[0]
#                 eof = cmd[1]
#                 uart.send(cmd[0])

#             while uart.any():
#                 data = uart.read()
#                 if data == eof:
#                     self.queue.pop()
#                     self.result[cmd[0]] = cmd[1]
#                     cmd = None
#                     break

#             cmd[1].append(data)

#     def recv(self, command='AT\n'):
#         if command in self.result:
#             return self.result[command]
#         return None

#     def send(self, command='AT\n', eof='\n'):
#         if data not in self.result:
#             self.queue.append((data, eof))

#     def bind(command, function):
#         func_set[command] = function

#     def work():
#         pass

# if __name__ == "__main__":
#     host = UartHost(uart)
#     pass
