import time
from machine import UART

uart = UART(2)  # UART(2) RX16 TX17
uart.init(57600, bits=8, parity=None, stop=1)

uart.write('hello world')
while True:
    recvlen = uart.any()
    if time.time() % 5 == 0:
        if recvlen > 0:
            time.sleep_ms(1000)
            print('------')
            buffer = uart.read(recvlen)
            uart.write(buffer)
            print(buffer)
