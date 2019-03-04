from machine import UART
import utime
from machine import Pin

class M5310_A():
    def send_cmd(self,cmd):
        self.uart.write(cmd + '\r\n')
    def cheak_ack(self,buf, ack):
        if ack in buf:
            return True
        else:
            return False
    def __init__(self):
        self.rst = Pin(18, Pin.OUT)
        self.uart = UART(2)
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self.RecvMax = 128
        self.RecvBuf = bytearray()
        self.cmd = ['AT', 'AT+CIMI', 'AT+COPS=1,2,\"46000\"', 'AT+CSQ', 'AT+CEREG?', 'AT+CGATT?',
               'AT+NSOCR="DGRAM",17,0,1', 'AT+NSOCFG=0', 'AT+NSOCFG=0,0,0']
        self.cmd_len = len(self.cmd)
        self.cmd_index = 0
        self.set_up()
    def set_up(self):
        self.rst.value(1)
        utime.sleep_ms(200)
        self.rst.value(0)
        self.send_cmd(self.cmd[self.cmd_index])
        send_time = utime.ticks_ms()
        while True:
            recvlen = self.uart.any()
            if recvlen > 0:
                buffer = self.uart.read(recvlen)
                for data in buffer:
                    self.RecvBuf.append(data)
                if self.cmd[self.cmd_index] == 'AT' or self.cmd[self.cmd_index] == 'AT+CIMI' \
                        or self.cmd[self.cmd_index] == 'AT+COPS=1,2,\"46000\"' or self.cmd[self.cmd_index] ==\
                        'AT+NSOCFG=0' or self.cmd[self.cmd_index] == 'AT+NSOCFG=0,0,0':
                    if self.cheak_ack(self.RecvBuf, b'\r\nOK\r\n'):
                        print('CHEAK_OK')
                        print(self.RecvBuf)
                        self.RecvBuf = bytearray()
                        self.cmd_index += 1
                        if self.cmd_index >= self.cmd_len:
                            break
                        else:
                            self.send_cmd(self.cmd[self.cmd_index])
                            send_time = utime.ticks_ms()
                elif self.cmd[self.cmd_index] == 'AT+CSQ':
                    if self.cheak_ack(self.RecvBuf, b'\r\n+CSQ:'):
                        print('CHEAK_OK')
                        print(self.RecvBuf)
                        strbuf = bytes(self.RecvBuf)
                        print(strbuf)
                        num = strbuf.find(b':')
                        csq = int(strbuf[num + 1:num + 3])
                        if csq > 12 and csq < 99:
                            self.RecvBuf = bytearray()
                            self.cmd_index += 1
                            if self.cmd_index >= self.cmd_len:
                                break
                            else:
                                self.send_cmd(self.cmd[self.cmd_index])
                                send_time = utime.ticks_ms()
                elif self.cmd[self.cmd_index] == 'AT+CGATT?':
                    if self.cheak_ack(self.RecvBuf, b'+CGATT:1'):
                        print('CHEAK_OK')
                        print(self.RecvBuf)
                        self.RecvBuf = bytearray()
                        self.cmd_index += 1
                        if self.cmd_index >= self.cmd_len:
                            break
                        else:
                            self.send_cmd(self.cmd[self.cmd_index])
                            send_time = utime.ticks_ms()
                elif self.cmd[self.cmd_index] == 'AT+CEREG?':
                    if self.cheak_ack(self.RecvBuf, b'+CEREG:0'):
                        print('CHEAK_OK')
                        print(self.RecvBuf)

                        strbuf = bytes(self.RecvBuf)
                        print(strbuf)
                        num = strbuf.find(b'G:')
                        reg = int(strbuf[num + 4:num + 5])
                        if reg == 1 or reg == 5:
                            self.RecvBuf = bytearray()
                            self.cmd_index += 1
                            if self.cmd_index >= self.cmd_len:
                                break
                            else:
                                self.send_cmd(self.cmd[self.cmd_index])
                                send_time = utime.ticks_ms()
                elif self.cmd[self.cmd_index] == 'AT+NSOCR="DGRAM",17,0,1':
                    if self.cheak_ack(self.RecvBuf, b'\r\nOK\r\n'):
                        print('CHEAK_OK')
                        print(self.RecvBuf)
                        strbuf = bytes(self.RecvBuf)
                        print(strbuf)
                        num = strbuf.find(b'\r\nOK\r\n')
                        reg = int(strbuf[num - 3]) - 48
                        print(reg)
                        if reg >= 0 and reg <= 6:
                            self.RecvBuf = bytearray()
                            self.cmd_index += 1
                            if self.cmd_index >= self.cmd_len:
                                break
                            else:
                                self.send_cmd(self.cmd[self.cmd_index])
                                send_time = utime.ticks_ms()
            if (len(self.RecvBuf) > self.RecvMax):
                self.RecvBuf = bytearray()
                print('OUT LINE')
                self.send_cmd(self.cmd[self.cmd_index])
                print('resend:', self.cmd[self.cmd_index])
                send_time = utime.ticks_ms()
            now_time = utime.ticks_ms()
            if send_time + 500 < now_time:
                self.RecvBuf = bytearray()
                self.send_cmd(self.cmd[self.cmd_index])
                print('resend:', self.cmd[self.cmd_index])
                send_time = utime.ticks_ms()
    def send_data(self,data):
            data='AT+NSOST=0,zwidas.top,8888,,\"%s\"'%data
            self.send_cmd(data)

def unit_test():
    ts=M5310_A()
    ts.send_data('hello')
    while True:
        recvlen = ts.uart.any()
        if recvlen > 0:
            buffer = ts.uart.read(recvlen)
            for data in buffer:
                ts.RecvBuf.append(data)
            print(ts.RecvBuf)
            if ts.cheak_ack(ts.RecvBuf, b'+NSONMI'):
                ts.RecvBuf=bytearray()
                ts.send_cmd('AT+NSORF=0,100')

if __name__=='__main__':
    unit_test()