import time
from machine import UART

uart = UART(2)  # UART(2) RX16 TX17
uart.init(57600, bits=8, parity=None, stop=1)

time.sleep(1)
uart.write("hello\n")

while True:
    recvlen = uart.any()
    if recvlen > 0:
        uart.write(uart.read(recvlen))
